import os
import subprocess
import sys
import requests
import click
import pkg_resources


from dotenv import load_dotenv
from src.utils.prepare_headers import get_api_url_and_prepare_headers_version_control
from src.utils.message_utils import (
    prepare_error_message,
    prepare_success_message,
    prepare_warning_message,
)
from src.utils.consts.message_consts import (
    TIMEOUT_ERROR,
    UNEXPECTED_ERROR,
    OUTDATED_MAJOR,
    OUTDATED_MINOR,
)


ENV_FILE_PATH = pkg_resources.resource_filename("src", ".env")
load_dotenv(dotenv_path=ENV_FILE_PATH, verbose=True)

MAJOR_VERSION = int(os.getenv("MAJOR_VERSION"))
MINOR_VERSION = int(os.getenv("MINOR_VERSION"))


def check_version():
    """Checks if Client version is up to date with Server version."""
    url, headers = get_api_url_and_prepare_headers_version_control()
    try:
        res = requests.get(
            url,
            headers=headers,
            timeout=10,
        )
    except requests.exceptions.ReadTimeout:
        click.echo(prepare_error_message(TIMEOUT_ERROR))
        sys.exit()

    if res.status_code != 200:
        click.echo(prepare_error_message(UNEXPECTED_ERROR))
        sys.exit()

    data = res.json()
    if data["server_version"]["major"] > MAJOR_VERSION:
        click.echo(prepare_error_message(OUTDATED_MAJOR))
        while True:
            anwser = input("Update now? (Y/N): ").lower()
            if anwser in ("y", "yes"):
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "cgcsdk"]
                )
                click.echo(prepare_success_message("Update successful!"))
                break
            if anwser in ("n", "no"):
                sys.exit()
    elif data["server_version"]["minor"] > MINOR_VERSION:
        click.echo(prepare_warning_message(OUTDATED_MINOR))


def get_version():
    """Returns version of cgcsdk."""
    return f"{MAJOR_VERSION}.{MINOR_VERSION}"
