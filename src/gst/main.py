# -*- coding: utf-8 -*-

import click

from gst.commands import auth, logout


@click.group()
@click.version_option(
    version="0.1.0",
    prog_name="gst",
)
def cli():
    """gst: A CLI tool to manage your GitHub starred repositories."""
    pass


cli.add_command(auth)
cli.add_command(logout)
