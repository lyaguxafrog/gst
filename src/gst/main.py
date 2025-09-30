# -*- coding: utf-8 -*-

import importlib.metadata

import click

from gst.commands import auth, clone_gist, create_gist, logout


__version__ = importlib.metadata.version("gist-cli")


@click.group()
@click.version_option(
    version=__version__,
    prog_name="gst",
)
def cli():
    """gst: A CLI tool to manage your GitHub Gists."""
    pass


cli.add_command(auth)
cli.add_command(logout)
cli.add_command(create_gist)
cli.add_command(clone_gist)
