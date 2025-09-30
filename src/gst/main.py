# -*- coding: utf-8 -*-

import importlib.metadata

import click

from gst.commands import auth, logout


__version__ = importlib.metadata.version("gst")


@click.group()
@click.version_option(
    version=__version__,
    prog_name="gst",
)
def cli():
    """gst: A CLI tool to manage your GitHub starred repositories."""
    pass


cli.add_command(auth)
cli.add_command(logout)
