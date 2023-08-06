# -*- coding: utf-8 -*-
import http.client as http_client
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def retry_session(headers, retries=4, backoff_factor=1, status_forcelist=(500, 502, 504), session=None, upload=False):
    # We don't need to see every byte being uploaded in verbose mode
    if os.environ.get('DEBUG_HTTP') and upload is False:
        http_client.HTTPConnection.debuglevel = 5
    else:
        http_client.HTTPConnection.debuglevel = 0

    requests.Session()
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        status=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        method_whitelist=['HEAD', 'TRACE', 'GET', 'PUT', 'OPTIONS', 'DELETE', 'POST']
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update(headers)
    return session
