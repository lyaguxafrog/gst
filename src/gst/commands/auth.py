# -*- coding: utf-8 -*-

import getpass

import click
from click import echo

from gst.services.token_setter import get_token, set_token


@click.command()
def auth():
    """Authenticate with GitHub by providing a personal access token."""
    echo(
        "To generate a personal access token, visit: https://github.com/settings/personal-access-tokens"
    )
    token = getpass.getpass("Token: ")
    set_token(token)
    echo("Token saved successfully!")


@click.command()
def logout():
    """Logout by removing the stored personal access token."""
    try:
        get_token()  # Check if a token exists
        set_token("")  # Clear the token
        echo("Logged out successfully!")
    except ValueError:
        echo("No token found. You are already logged out.")
