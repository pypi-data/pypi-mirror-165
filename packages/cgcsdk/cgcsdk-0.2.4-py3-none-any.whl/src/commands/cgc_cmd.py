import click

from src.commands.compute.compute_cmd import compute_delete
from src.utils.click_group import CustomCommand


@click.command("rm", cls=CustomCommand)
@click.argument("name", type=click.STRING)
def cgc_rm(name: str):
    """
    Delete a compute pod in user namespace
    \f
    :param name: name of pod to delete
    :type name: str
    """
    compute_delete(name)
