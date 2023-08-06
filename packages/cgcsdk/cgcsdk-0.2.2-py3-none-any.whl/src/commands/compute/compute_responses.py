import json
import requests


from src.telemetry.basic import increment_metric
from src.telemetry.basic import change_gauge
from src.utils.message_utils import prepare_error_message, prepare_success_message
from src.utils.config_utils import get_namespace
from src.utils.response_utils import response_precheck
from src.utils.consts.message_consts import UNEXPECTED_ERROR


def compute_create_filebrowser_response(response: requests.Response) -> str:
    """Create response string for compute create_filebrowser command

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    try:
        metric_ok = f"{get_namespace()}.compute.create_filebrowser.ok"
        metric_error = f"{get_namespace()}.compute.create_filebrowser.error"
        response_precheck(response, metric_error)

        if response.status_code == 200:
            message = "Filebrowser created successfuly!"
            increment_metric(metric_ok)
            return prepare_success_message(message)
        if response.status_code == 409:
            increment_metric(metric_error)
            message = "Filebrowser already exists in namespace."
            return prepare_error_message(message)
    except (KeyError, json.JSONDecodeError):
        increment_metric(metric_error)
        return prepare_error_message(UNEXPECTED_ERROR)


def compute_create_error_parser(error: dict) -> str:
    """Function that pases error from API for compute create command.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """
    # TODO add errors after backend is finished
    # print(error)
    try:

        if error["reason"] == "COMPUTE_TEMPLATE_NAME_ALREADY_EXISTS":
            message = f"Compute pod with name {error['details']['name']} already exists in namespace."
            return prepare_error_message(message)
        if error["reason"] == "PVC_NOT_FOUND":
            message = f"Volume {error['details']['pvc_name']} does not exist. Pod creation failed."
            return prepare_error_message(message)
        if error["reason"] == "COMPUTE_CREATE_FAILURE":
            message = f"Entity template {error['details']['pvc_name']} not found. Pod creation failed."
            return prepare_error_message(message)
        if error["reason"] == "Invalid":
            message = "Invalid app name, for more information refer to: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/"
            return prepare_error_message(message)
        message = prepare_error_message(error)
        return message
    except KeyError:
        return prepare_error_message(UNEXPECTED_ERROR)


def compute_create_response(response: requests.Response) -> str:
    """Create response string for compute create command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    try:
        metric_ok = f"{get_namespace()}.compute.create.ok"
        metric_error = f"{get_namespace()}.compute.create.error"
        response_precheck(response, metric_error)

        data = json.loads(response.text)

        if response.status_code == 200:
            increment_metric(metric_ok)
            change_gauge(f"{get_namespace()}.compute.count", 1)

            name = data["details"]["created_service"]["name"]
            entity = data["details"]["created_service"]["labels"]["entity"]
            volume_list = data["details"].get("mounted_pvc_list")
            volumes = ",".join(volume_list) if volume_list else None
            try:
                jupyter_token = data["details"]["created_template"]["jupyter_token"]
            except KeyError:
                jupyter_token = None
            pod_url = data["details"]["created_template"]["pod_url"]
            # TODO bedzie wiecej entity jupyterowych
            if entity == "tensorflow-jupyter":
                message = f"{entity} Pod {name} has been created! Mounted volumes: {volumes}\nAccessible at: {pod_url}\nJupyter token: {jupyter_token}"
            else:
                message = (
                    f"{entity} Pod {name} has been created! Mounted volumes: {volumes}"
                )
            return prepare_success_message(message)

        increment_metric(metric_error)
        error = compute_create_error_parser(data)
        return error
    except (KeyError, json.JSONDecodeError):
        increment_metric(metric_error)
        return prepare_error_message(UNEXPECTED_ERROR)


def compute_delete_error_parser(error: dict) -> str:
    """Function that pases error from API for compute delete command.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """
    try:
        if error["reason"] == "NOT_DELETED_ANYTHING_IN_COMPUTE_DELETE":
            message = f"Pod with name {error['details']['name']} does not exist."
            return prepare_error_message(message)
        message = prepare_error_message(error)
        return message
    except KeyError:
        return prepare_error_message(UNEXPECTED_ERROR)


def compute_delete_response(response: requests.Response) -> str:
    """Create response string for compute delete command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    try:
        metric_ok = f"{get_namespace()}.compute.delete.ok"
        metric_error = f"{get_namespace()}.compute.delete.error"
        response_precheck(response, metric_error)

        data = json.loads(response.text)

        if response.status_code == 200:
            name = data["details"]["deleted_service"]["name"]
            increment_metric(metric_ok)
            change_gauge(f"{get_namespace()}.compute.count", -1)
            message = f"Pod {name} successfully deleted with their service."
            return prepare_success_message(message)
        else:
            increment_metric(metric_error)
            error = compute_delete_error_parser(data)
            return error
    except (KeyError, json.JSONDecodeError):
        increment_metric(metric_error)
        return prepare_error_message(UNEXPECTED_ERROR)
