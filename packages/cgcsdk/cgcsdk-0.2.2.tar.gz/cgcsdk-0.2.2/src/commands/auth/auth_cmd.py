import os
import shutil
import pkg_resources
import click
import requests
from dotenv import load_dotenv

from src.utils.config_utils import get_config_path, get_namespace
from src.utils.config_utils import add_to_config
from src.utils.prepare_headers import get_api_url_and_prepare_headers_register
from src.telemetry.basic import increment_metric
from src.utils.message_utils import prepare_error_message, prepare_success_message
from src.commands.auth import auth_utils
from src.utils.cryptography import rsa_crypto
from src.utils.click_group import CustomCommand
from src.utils.consts.message_consts import TIMEOUT_ERROR


ENV_FILE_PATH = pkg_resources.resource_filename("src", ".env")
load_dotenv(dotenv_path=ENV_FILE_PATH, verbose=True)
TMP_DIR = os.path.join(get_config_path(), os.getenv("TMP_DIR"))


@click.command("register", cls=CustomCommand)
@click.option("--user_id", "-u", "user_id", prompt=True)
@click.option("--access_key", "-k", "access_key", prompt=True)
def auth_register(user_id: str, access_key: str):
    """Register a user in system using user id and access key.
    \f
    :param user_id: username received in invite
    :type user_id: str
    :param access_key: access key received in invite
    :type access_key: str
    """

    url, headers = get_api_url_and_prepare_headers_register(user_id, access_key)
    pub_key_bytes, priv_key_bytes = rsa_crypto.key_generate_pair()
    payload = pub_key_bytes

    try:
        res = requests.post(
            url,
            data=payload,
            headers=headers,
            allow_redirects=True,
            timeout=10,
        )

        if res.status_code != 200:
            increment_metric("auth.register.error")
            if res.status_code == 401:
                message = "Could not validate user id or access key."
                click.echo(prepare_error_message(message))
                return

            message = "Could not register user. Please try again or contact support at support@comtegra.pl."
            click.echo(prepare_error_message(message))
            return

        unzip_dir = auth_utils.save_and_unzip_file(res)
        aes_key, passwd = auth_utils.get_aes_key_and_passwd(unzip_dir, priv_key_bytes)

        add_to_config(user_id=user_id, passwd=passwd, aes_key=aes_key)
        auth_utils.auth_create_api_key()

        message = f"Register successful! You can now use the CLI. Config file is saved in {get_config_path()}"
        click.echo(prepare_success_message(message))
        increment_metric(f"{get_namespace()}.auth.register.ok")
        shutil.rmtree(TMP_DIR)
    except requests.exceptions.ReadTimeout:
        click.echo(prepare_error_message(TIMEOUT_ERROR))
