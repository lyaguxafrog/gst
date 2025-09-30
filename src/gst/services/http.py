# -*- coding: utf-8 -*-

from typing import Literal

import httpx


__ENDPOINT__: str = "https://api.github.com/gists"


def send_request(
    method: Literal["POST", "GET"],
    headers: dict[str, str],
    path: str | None = None,
    body: dict[str, str] | None = None,
) -> httpx.Response:
    """Send an HTTP request to the specified endpoint.

    Args:
        method (Literal["POST", "GET"]): The HTTP method to use.
        headers (dict[str, str]): The headers to include in the request.
        path (str | None): The path to append to the endpoint (if any).
        body (dict[str, str] | None): The body of the request (for POST requests).

    Returns:
        httpx.Response: The response from the server.

    Raises:
        ValueError: If an unsupported HTTP method is provided.
    """
    if path:
        ENDPOINT = f"{__ENDPOINT__}/{path}"
    else:
        ENDPOINT = __ENDPOINT__

    with httpx.Client() as client:
        match method:
            case "POST":
                response = client.post(ENDPOINT, headers=headers, json=body)
            case "GET":
                response = client.get(ENDPOINT, headers=headers)
            case _:
                raise ValueError(f"Unsupported HTTP method: {method}")

    response.raise_for_status()
    return response
