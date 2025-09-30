# -*- coding: utf-8 -*-

import click

from gst.services.http import send_request
from gst.services.token_setter import get_token


@click.command(name="create", help="Create a new Gist.")
@click.argument("file_path", type=click.Path(exists=True))
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
def create_gist(
    file_path: str,
    description: str | None = None,
    web: bool = False,
    public: bool = False,
):
    """Create a new Gist with the specified file."""
    try:
        token = get_token()
    except ValueError as e:
        click.echo(f"Error: {e}")
        return

    with open(file_path) as file:
        content = file.read()

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    body = {
        "description": description if description else "",
        "public": public,
        "files": {file_path.split("/")[-1]: {"content": content}},
    }

    from icecream import ic

    ic(body)
    ic(headers)

    try:
        response = send_request("POST", headers, body)
        ic(response)
        gist_id = response.json().get("id")
        gist_url = f"https://gist.github.com/{gist_id}"
        click.echo("Gist created successfully!")
        click.echo(f"ID: {gist_id}")
        click.echo(f"URL: {gist_url}")
    except Exception as e:
        click.echo(f"Error creating Gist: {e}")
        return

    if web:
        import webbrowser

        webbrowser.open(gist_url)
