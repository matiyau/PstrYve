#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 17:35:36 2022.

@author: Nishad Mandlik
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class AccessRespHandler(BaseHTTPRequestHandler):
    """Handler for access response."""

    def do_GET(self):
        """
        Parse GET request received by the server.

        Returns
        -------
        None.

        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        params = parse_qs(urlparse(self.path).query, keep_blank_values=True)
        params = {k: v[0] for (k, v) in params.items()}
        self.server.access_resp = params


class AccessRespServer(HTTPServer):
    """Server for receiving response for an access request."""

    def __init__(self):
        self.access_resp = None
        port = 8000
        while (port < 8050):
            try:
                super().__init__(("localhost", port), AccessRespHandler)
                self.timeout = 120
                return
            except OSError:
                port += 1
                continue
        raise OSError(98, "Ports Not Available")

    def __del__(self):
        """
        Cleanup the server before destruction.

        Returns
        -------
        None.

        """
        self.server_close()
