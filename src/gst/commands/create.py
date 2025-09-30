# -*- coding: utf-8 -*-

import os
import webbrowser

import click

from gst.services.http import send_request
from gst.services.token_setter import get_token


def is_text_file(file_path: str) -> bool:
    """Check utf-8 text file by trying to read it."""
    try:
        with open(file_path, encoding="utf-8") as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False


@click.command(
    name="create", help="Create a new Gist from a file or directory."
)
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-d", "--description", default=None, help="Description of the Gist."
)
@click.option(
    "-w",
    "--web",
    is_flag=True,
    help="Open the Gist in a web browser after creation.",
)
@click.option("-p", "--public", is_flag=True, help="Make the Gist public.")
def create_gist(path: str, description: str | None, web: bool, public: bool):
    """Create a new Gist from a file or all files in a directory."""
    try:
        token = get_token()
    except ValueError as e:
        click.echo(f"Error: {e}")
        return

    files_payload = {}

    if os.path.isfile(path):
        if is_text_file(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()
            if content.strip():
                files_payload[os.path.basename(path)] = {"content": content}
            else:
                click.echo(f"⚠ Skipping empty file: {path}")
        else:
            click.echo(f"⚠ Skipping binary file: {path}")

    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if not is_text_file(file_path):
                    click.echo(f"⚠ Skipping binary file: {file_path}")
                    continue
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                if not content.strip():
                    click.echo(f"⚠ Skipping empty file: {file_path}")
                    continue
                rel_path = os.path.relpath(file_path, path).replace(os.sep, "_")
                files_payload[rel_path] = {"content": content}
    else:
        click.echo(f"Error: {path} is neither a file nor a directory.")
        return

    if not files_payload:
        click.echo("Error: No valid files to create Gist.")
        return

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    body = {
        "description": description if description else "",
        "public": public,
        "files": files_payload,
    }

    try:
        response = send_request("POST", headers, None, body)
        response.raise_for_status()
        gist_id = response.json().get("id")
        gist_url = f"https://gist.github.com/{gist_id}"
        click.echo("Gist created successfully!")
        click.echo(f"ID: {gist_id}")
        click.echo(f"URL: {gist_url}")
    except Exception as e:
        click.echo(f"Error creating Gist: {e}")
        return

    if web:
        webbrowser.open(gist_url)

    return
