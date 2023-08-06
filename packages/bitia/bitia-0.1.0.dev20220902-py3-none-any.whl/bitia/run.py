"""
Copyright (C) 2022 Subconscious Compute 'All rights reserved.'
"""

import typing as T

import bitia.common
import bitia.compose

def _url_validate(url):
    """URL validation"""
    from urllib.parse import urlparse

    o = urlparse(url)
    assert o is not None
    assert o.scheme in ["http", "https"]


def submit_job(
    user_input: str, *, server: T.Optional[str] = None, recreate: bool = False, **kwargs
):
    if server is None:
        server = bitia.config.server()
    _url_validate(server), "given server url is invalid, please enter a valid url"

    # Jobs are run on the server. It is here because we are testing it right
    # now.
    compose = bitia.compose.ComposeFile(user_input)
    for line in compose.run(recreate=recreate, **kwargs):
        print(line)
