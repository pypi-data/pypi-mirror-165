import os
import click
import pkg_resources
import requests
from tabulate import tabulate
from dotenv import load_dotenv


from src.commands.billing.billing_utils import (
    get_status_list_to_print,
    get_status_list_headers,
)
from src.telemetry.basic import increment_metric
from src.utils.config_utils import get_namespace
from src.utils.message_utils import prepare_error_message
from src.utils.prepare_headers import get_api_url_and_prepare_headers
from src.utils.response_utils import response_precheck
from src.utils.click_group import CustomGroup, CustomCommand
from src.utils.consts.message_consts import TIMEOUT_ERROR


ENV_FILE_PATH = pkg_resources.resource_filename("src", ".env")
load_dotenv(dotenv_path=ENV_FILE_PATH, verbose=True)


API_URL = os.getenv("API_URL")
CGC_SECRET = os.getenv("CGC_SECRET")


@click.group("billing", cls=CustomGroup)
def billing_group():
    """
    Access and manage billing information.
    """
    pass


@billing_group.command("status", cls=CustomCommand)
def billing_status():
    """
    Shows billing status for user namespace
    """
    metric_ok = f"{get_namespace()}.billing.status.ok"
    metric_error = f"{get_namespace()}.billing.status.error"

    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/billing/status"
    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=10,
        )

        response_precheck(response, metric_error)

        if response.status_code != 200:
            increment_metric(metric_error)
            message = "Error occuerd while getting billing status. Try again or contact us at support@comtegra.pl"
            click.echo(prepare_error_message(message))
            return

        data = response.json()
        total_cost = data["details"]["costs"]["cost_total"]
        namespace = data["details"]["namespace"]
        costs_list = data["details"]["costs"]["details"]
        if not costs_list:
            click.echo("No costs found")
            return

        costs_list_to_print = get_status_list_to_print(costs_list)
        list_headers = get_status_list_headers()
        click.echo(tabulate(costs_list_to_print, headers=list_headers))
        click.echo(f"\nTotal cost for namespace {namespace}: {total_cost:.2f}\n")
        increment_metric(metric_ok)
    except requests.exceptions.ReadTimeout:
        increment_metric(metric_error)
        click.echo(prepare_error_message(TIMEOUT_ERROR))


@billing_group.command("pay", cls=CustomCommand)
def billing_pay():
    """
    Interface for easy payment
    """
    click.echo("Initializing payment!")


@click.group("fvat", cls=CustomGroup)
def fvat_group():
    """
    Invoice management
    """
    pass


@fvat_group.command("ls", cls=CustomCommand)
def fvat_ls():
    """
    Lists all invoices for user namespace
    """
    click.echo("Listing all invoices!")


@fvat_group.command("id", cls=CustomCommand)
@click.argument(
    "invoice_id",
)
def fvat_id(invoice_id: str):
    """
    Opens invoice with given ID
    """
    click.echo(f"Opening invoice {invoice_id}!")


billing_group.add_command(fvat_group)
