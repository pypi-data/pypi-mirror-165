import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import dagster._check as check
import yaml
from dagster._core.test_utils import remove_none_recursively
from dagster._serdes.serdes import deserialize_json_to_dagster_namedtuple
from dagster._utils import DEFAULT_WORKSPACE_YAML_FILENAME, frozendict
from dagster._utils.merger import deep_merge_dicts
from dagster_cloud_cli import gql, ui
from dagster_cloud_cli.config_utils import (
    DEFAULT_LOCATION_LOAD_TIMEOUT,
    DEPLOYMENT_CLI_OPTIONS,
    dagster_cloud_options,
    get_location_document,
)
from dagster_cloud_cli.core.graphql_client import GqlShimClient
from dagster_cloud_cli.core.workspace import CodeDeploymentMetadata
from dagster_cloud_cli.utils import add_options, create_stub_command
from typer import Argument, Option, Typer

DEFAULT_LOCATIONS_YAML_FILENAME = "locations.yaml"

app = Typer(help="Manage your Dagster Cloud workspace.")


def _get_location_input(location: str, kwargs: Dict[str, Any]) -> gql.CliInputCodeLocation:
    python_file = kwargs.get("python_file")

    return gql.CliInputCodeLocation(
        name=location,
        python_file=str(python_file) if python_file else None,
        package_name=kwargs.get("package_name"),
        image=kwargs.get("image"),
        module_name=kwargs.get("module_name"),
        working_directory=kwargs.get("working_directory"),
        executable_path=kwargs.get("executable_path"),
        attribute=kwargs.get("attribute"),
        commit_hash=kwargs["git"].get("commit_hash")
        if "git" in kwargs
        else kwargs.get("commit_hash"),
        url=kwargs["git"].get("url") if "git" in kwargs else kwargs.get("git_url"),
    )


def _add_or_update_location(
    client: GqlShimClient,
    location_document: Dict[str, Any],
    location_load_timeout: int,
    agent_heartbeat_timeout: int,
) -> None:
    try:
        gql.add_or_update_code_location(client, location_document)
        name = location_document["location_name"]
        ui.print(f"Added or updated location {name}.")
        wait_for_load(
            client,
            [name],
            location_load_timeout=location_load_timeout,
            agent_heartbeat_timeout=agent_heartbeat_timeout,
        )
    except Exception as e:
        raise ui.error(str(e))


@app.command(name="add-location", short_help="Add or update a repo location image.")
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(DEPLOYMENT_CLI_OPTIONS)
def add_command(
    api_token: str,
    url: str,
    location_load_timeout: int,
    agent_heartbeat_timeout: int,
    location: str = Argument(None, help="Code location name."),
    **kwargs,
):
    """Add or update the image for a repository location in the workspace."""
    with gql.graphql_client_from_url(url, api_token) as client:
        location_document = get_location_document(location, kwargs)
        _add_or_update_location(
            client,
            location_document,
            location_load_timeout=location_load_timeout,
            agent_heartbeat_timeout=agent_heartbeat_timeout,
        )


def list_locations(location_names: List[str]) -> str:
    if len(location_names) == 0:
        return ""
    elif len(location_names) == 1:
        return location_names[0]
    else:
        return f"{', '.join(location_names[:-1])}, and {location_names[-1]}"


@app.command(name="update-location", short_help="Update a repo location image.")
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(DEPLOYMENT_CLI_OPTIONS)
def update_command(
    api_token: str,
    url: str,
    location_load_timeout: int,
    agent_heartbeat_timeout: int,
    location: str = Argument(None, help="Code location name."),
    **kwargs,
):
    """Update the image for a repository location in the workspace."""
    with gql.graphql_client_from_url(url, api_token) as client:
        location_document = get_location_document(location, kwargs)
        _add_or_update_location(
            client,
            location_document,
            location_load_timeout=location_load_timeout,
            agent_heartbeat_timeout=agent_heartbeat_timeout,
        )


def wait_for_load(
    client,
    locations,
    location_load_timeout=DEFAULT_LOCATION_LOAD_TIMEOUT,
    agent_heartbeat_timeout=DEFAULT_LOCATION_LOAD_TIMEOUT,
):
    start_time = time.time()
    ui.print(f"Waiting for agent to sync changes to {list_locations(locations)}...")

    if not location_load_timeout and not agent_heartbeat_timeout:
        return

    has_agent_heartbeat = False
    while True:
        if not has_agent_heartbeat:
            if time.time() - start_time > agent_heartbeat_timeout:
                raise ui.error(
                    "No Dagster Cloud agent is actively heartbeating. Make sure that you have a Dagster Cloud agent running."
                )
            try:
                agents = gql.fetch_agent_status(client)
            except Exception as e:
                raise ui.error("Unable to query agent status: " + str(e))

            has_agent_heartbeat = any(a["status"] == "RUNNING" for a in agents)

        if time.time() - start_time > location_load_timeout:
            raise ui.error("Timed out waiting for location data to update.")

        try:
            nodes = gql.fetch_code_locations(client)
        except Exception as e:
            raise ui.error(str(e))

        nodes_by_location = {node["name"]: node for node in nodes}

        if all(
            location in nodes_by_location
            and nodes_by_location[location].get("loadStatus") == "LOADED"
            for location in locations
        ):

            error_locations = [
                location
                for location in locations
                if "locationOrLoadError" in nodes_by_location[location]
                and nodes_by_location[location]["locationOrLoadError"]["__typename"]
                == "PythonError"
            ]

            if error_locations:
                error_string = "Some locations failed to load after being synced by the agent:\n" + "\n".join(
                    [
                        f"Error loading {error_location}: {str(nodes_by_location[error_location]['locationOrLoadError'])}"
                        for error_location in error_locations
                    ]
                )
                raise ui.error(error_string)
            else:
                ui.print(
                    f"Agent synced changes to {list_locations(locations)}. Changes should now be visible in dagit."
                )
                break

        time.sleep(3)


@app.command(
    name="delete-location",
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def delete_command(
    api_token: str,
    url: str,
    location: str = Argument(..., help="Code location name."),
):
    """Delete a repository location from the workspace."""
    with gql.graphql_client_from_url(url, api_token) as client:
        try:
            gql.delete_code_location(client, location)
            ui.print(f"Deleted location {location}.")
        except Exception as e:
            raise ui.error(str(e))


@app.command(
    name="list",
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def list_command(
    url: str,
    api_token: str,
):
    """List repository locations in the workspace."""
    with gql.graphql_client_from_url(url, api_token) as client:
        execute_list_command(client)


def execute_list_command(client):
    list_res = gql.fetch_workspace_entries(client)

    ui.print("Listing locations...")

    for location in list_res:
        metadata = check.inst(
            deserialize_json_to_dagster_namedtuple(location["serializedDeploymentMetadata"]),
            CodeDeploymentMetadata,
        )

        location_desc = [location["locationName"]]
        if metadata.python_file:
            location_desc.append(f"File: {metadata.python_file}")
        if metadata.package_name:
            location_desc.append(f"Package: {metadata.package_name}")
        if metadata.image:
            location_desc.append(f"Image: {metadata.image}")

        ui.print("\t".join(location_desc))


@app.command(name="pull")
@dagster_cloud_options(allow_empty=True, requires_url=True)
def pull_command(
    url: str,
    api_token: str,
):
    """Retrieve code location definitions as a workspace.yaml file."""
    with gql.graphql_client_from_url(url, api_token) as client:
        document = gql.fetch_locations_as_document(client)
        ui.print_yaml(document or {})


@app.command(name="sync", short_help="Sync workspace with a workspace.yaml file.")
@dagster_cloud_options(allow_empty=True, requires_url=True)
def sync_command(
    url: str,
    api_token: str,
    location_load_timeout: int,
    agent_heartbeat_timeout: int,
    workspace: Path = Option(
        DEFAULT_WORKSPACE_YAML_FILENAME,
        "--workspace",
        "-w",
        exists=True,
        help="Path to workspace file.",
    ),
):
    """Sync the workspace with the contents of a workspace.yaml file."""
    with gql.graphql_client_from_url(url, api_token) as client:
        execute_sync_command(
            client,
            workspace,
            location_load_timeout=location_load_timeout,
            agent_heartbeat_timeout=agent_heartbeat_timeout,
        )


def format_workspace_config(workspace_config) -> Dict[str, Any]:
    """Ensures the input workspace config is in the modern format, migrating an input
    in the old format if need be."""
    check.dict_param(workspace_config, "workspace_config")

    if isinstance(workspace_config.get("locations"), (dict, frozendict)):
        # Convert legacy formatted locations to modern format
        updated_locations = []
        for name, location in workspace_config["locations"].items():
            new_location = {
                k: v
                for k, v in location.items()
                if k not in ("python_file", "package_name", "module_name")
            }
            new_location["code_source"] = {}
            if "python_file" in location:
                new_location["code_source"]["python_file"] = location["python_file"]
            if "package_name" in location:
                new_location["code_source"]["package_name"] = location["package_name"]
            if "module_name" in location:
                new_location["code_source"]["module_name"] = location["module_name"]

            new_location["location_name"] = name
            updated_locations.append(new_location)
        return {"locations": updated_locations}
    else:
        check.is_list(workspace_config.get("locations"))
        return workspace_config


def execute_sync_command(client, workspace, location_load_timeout, agent_heartbeat_timeout):
    with open(str(workspace), "r", encoding="utf8") as f:
        config = yaml.load(f.read(), Loader=yaml.SafeLoader)
        processed_config = format_workspace_config(config)

    try:
        locations = gql.reconcile_code_locations(client, processed_config)
        ui.print(f"Synced locations: {', '.join(locations)}")
        wait_for_load(
            client,
            locations,
            location_load_timeout=location_load_timeout,
            agent_heartbeat_timeout=agent_heartbeat_timeout,
        )
    except Exception as e:
        raise ui.error(str(e))


try:
    from dagster_cloud.workspace.cli import snapshot_command

    app.command(name="snapshot", hidden=True)(snapshot_command)
except ImportError:
    app.command(name="snapshot", hidden=True)(create_stub_command("dagster-cloud"))
