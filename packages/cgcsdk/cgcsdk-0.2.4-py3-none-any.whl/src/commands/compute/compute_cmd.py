import json
import requests
import click
from tabulate import tabulate

from src.commands.compute.compute_responses import (
    compute_create_filebrowser_response,
    compute_create_response,
    compute_delete_response,
)
from src.commands.compute.data_model import (
    compute_create_payload_validator,
    compute_delete_payload_validator,
)
from src.commands.compute.compute_utills import list_get_pod_list_to_print
from src.utils.prepare_headers import get_api_url_and_prepare_headers
from src.telemetry.basic import increment_metric, setup_gauge
from src.utils.message_utils import prepare_error_message
from src.utils.config_utils import get_namespace
from src.utils.response_utils import response_precheck
from src.utils.click_group import CustomGroup, CustomCommand
from src.utils.consts.message_consts import TIMEOUT_ERROR


@click.group(name="compute", cls=CustomGroup)
@click.option("--debug", "debug", is_flag=True, default=False, hidden=True)
@click.pass_context
def compute_group(ctx, debug):
    """
    Management of compute resources.
    """
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@click.group(name="filebrowser", cls=CustomGroup)
def filebrowser_group():
    """
    Management of filebrowser.
    """


@filebrowser_group.command("create", cls=CustomCommand)
def compute_filebrowser_create():
    """Create a filebrowser service"""
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/compute/filebrowser_create"

    try:
        res = requests.post(
            url=url,
            headers=headers,
            timeout=10,
        )
        click.echo(compute_create_filebrowser_response(res))
    except requests.exceptions.ReadTimeout:
        increment_metric(f"{get_namespace()}.compute.create_filebrowser.error")
        click.echo(prepare_error_message(TIMEOUT_ERROR))


@filebrowser_group.command("delete", cls=CustomCommand)
def compute_filebrowser_delete():
    """Delete a filebrowser service"""
    compute_delete("filebrowser")


@compute_group.command("create", cls=CustomCommand)
@click.argument("entity", type=click.Choice(["tensorflow-jupyter", "nvidia-rapids"]))
@click.option("-n", "--name", "name", type=click.STRING, required=True)
@click.option("-g", "--gpu", "gpu", type=click.IntRange(0, 8), default=0)
@click.option(
    "-gt",
    "--gpu-type",
    "gpu_type",
    type=click.Choice(["A100", "V100", "A5000"], case_sensitive=False),
    default="V100",
)
@click.option("-c", "--cpu", "cpu", type=click.INT, default=1)
@click.option("-m", "--memory", "memory", type=click.INT, default=2)
@click.option("-v", "--volume", "volumes", multiple=True)
def compute_create(
    entity: str,
    gpu: int,
    gpu_type: str,
    cpu: int,
    memory: int,
    volumes: list[str],
    name: str,
):
    """
    Create a compute pod in user namespace.
    \f
    :param entity: name of entity to create
    :type entity: str
    :param gpu: number of gpus to be used by pod
    :type gpu: int
    :param cpu: number of cores to be used by pod
    :type cpu: int
    :param memory: GB of memory to be used by pod
    :type memory: int
    :param volumes: list of volumes to mount
    :type volumes: list[str]
    :param name: name of pod
    :type name: str
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/compute/create"

    payload = compute_create_payload_validator(
        name=name,
        entity=entity,
        cpu=cpu,
        memory=memory,
        gpu=gpu,
        volumes=volumes,
        gpu_type=gpu_type,
    )

    try:
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(compute_create_response(res))
    except requests.exceptions.ReadTimeout:
        increment_metric(f"{get_namespace()}.compute.create.error")
        click.echo(prepare_error_message(TIMEOUT_ERROR))


@compute_group.command("delete", cls=CustomCommand)
@click.argument("name", type=click.STRING)
def compute_delete_cmd(name: str):
    """
    Delete a compute pod from user namespace.
    \f
    :param name: name of pod to delete
    :type name: str
    """
    compute_delete(name)


def compute_delete(name: str):
    """
    Delete a compute pod using backend endpoint.
    \f
    :param name: name of pod to delete
    :type name: str
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/compute/delete"
    payload = compute_delete_payload_validator(name=name)
    try:
        res = requests.delete(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(compute_delete_response(res))
    except requests.exceptions.ReadTimeout:
        increment_metric(f"{get_namespace()}.compute.delete.error")
        click.echo(prepare_error_message(TIMEOUT_ERROR))


@compute_group.command("list", cls=CustomCommand)
@click.option(
    "-d", "--detailed", "detailed", type=click.BOOL, is_flag=True, default=False
)
@click.pass_context
def compute_list(ctx, detailed: bool):
    """
    List all pods for user namespace.
    """
    metric_ok = f"{get_namespace()}.compute.list.ok"
    metric_error = f"{get_namespace()}.compute.list.error"

    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/compute/list"
    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=10,
        )
        response_precheck(response, metric_error)

        if response.status_code != 200:
            increment_metric(metric_error)
            message = "Error occuerd while listing pods. Try again or contact us at support@comtegra.pl"
            click.echo(prepare_error_message(message))
            return

        data = response.json()
        pod_list = data["details"]["pods_list"]

        setup_gauge(f"{get_namespace()}.compute.count", len(pod_list))
        increment_metric(metric_ok)

        if not pod_list:
            click.echo("No pods to list.")
            return

        pod_list_to_print = list_get_pod_list_to_print(pod_list, detailed)

        list_headers = [
            "name",
            "type",
            "status",
            "volumes mounted",
            "CPU cores",
            "RAM",
            "GPU type",
            "GPU count",
            "URL",
            "Jupyter token",
        ]
        if not detailed:
            list_headers.remove("Jupyter token")

        if ctx.obj["DEBUG"]:
            print(pod_list_to_print)
        else:
            click.echo(tabulate(pod_list_to_print, headers=list_headers))

    except requests.exceptions.ReadTimeout:
        increment_metric(metric_error)
        click.echo(prepare_error_message(TIMEOUT_ERROR))


compute_group.add_command(filebrowser_group)
