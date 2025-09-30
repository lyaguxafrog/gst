# -*- coding: utf-8 -*-

import os

import click

from gst.services.http import send_request


@click.command(name="clone", help="Clone a Gist.")
@click.argument("gist", type=str, required=True)
@click.argument("path", type=click.Path(), default=".", required=False)
def clone_gist(gist: str, path: str):
    """Clone a Gist by its ID or URL into the specified directory."""
    if gist.startswith("http"):
        gist = gist.split("/")[-1]

    os.makedirs(path, exist_ok=True)

    data = send_request(
        method="GET",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        path=gist,
    )

    files = data.json().get("files", {})
    for filename, fileinfo in files.items():
        file_path = os.path.join(path, filename)
        with open(file_path, "w") as f:
            f.write(fileinfo.get("content", ""))
        click.echo(f"Created file: {file_path}")
    click.echo("Gist cloned successfully.")
