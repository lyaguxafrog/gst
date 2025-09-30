# -*- coding: utf-8 -*-

from typing import Literal

import httpx


__ENDPOINT__: str = "https://api.github.com/gists"


async def send_request(
    method: Literal["POST", "GET"],
    headers: dict[str, str],
    body: dict[str, str] | None = None,
) -> httpx.Response:
    """Send an HTTP request to the specified endpoint.

    Args:
        method (Literal["POST", "GET"]): The HTTP method to use.
        headers (dict[str, str]): The headers to include in the request.
        body (dict[str, str] | None): The body of the request (for POST requests).

    Returns:
        httpx.Response: The response from the server.
    """
    async with httpx.AsyncClient() as client:
        match method:
            case "POST":
                response = await client.post(
                    __ENDPOINT__, headers=headers, json=body
                )
            case "GET":
                response = await client.get(__ENDPOINT__, headers=headers)
            case "_":
                raise ValueError("Unsupported HTTP method")

    return response
