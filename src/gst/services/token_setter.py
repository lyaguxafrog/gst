# -*- coding: utf-8 -*-

import keyring


def set_token(token: str) -> None:
    """Store the provided token securely using the keyring library.

    Args:
        token (str): The token to be stored.
    """
    SERVICE = "gst"
    USERNAME = "github"
    keyring.set_password(SERVICE, USERNAME, token)


def get_token() -> str:
    """Retrieve the stored token from the keyring.

    Returns:
        str: The retrieved token.
    """
    SERVICE = "gst"
    USERNAME = "github"
    token = keyring.get_password(SERVICE, USERNAME)
    if token is None:
        raise ValueError("No token found. Please set a token first.")
    return token
