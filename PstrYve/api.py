#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 14:58:13 2022.

@author: Nishad Mandlik
"""

from .config import Cfg
from . import consts as c
from .enums import AccessScope, Sport, TokenType, ActivityFileType
from .server import AccessRespServer
from .web_view import WebApp
from requests import Request, post
from threading import Thread
import time


class API():
    """Class for interfacing with the Strava API."""

    def __init__(self, client_id, scope):
        self.cfg = Cfg(client_id)

        rfsh_tkn_valid = True

        if (not self.cfg.has_opt(c.CSCRT)):
            print("Client Secret Not Found. Please Enter Client Secret:")
            cscrt = input()
            self.cfg.set_opt(c.CSCRT, cscrt)
            rfsh_tkn_valid = False

        if scope.check_flags(self.cfg.get_opt(c.SCOPE)):
            rfsh_tkn_valid = False

        if not rfsh_tkn_valid:
            resp = self._request_access(scope)
            if (resp is None or
                    (not scope.check_flags(resp.get("scope", None)))):
                raise RuntimeError("Scope Access Not Granted")

            # Granted scope may be wider than the requested one.
            # Hence, update the scope variable
            scope = AccessScope.from_str(resp["scope"])

            resp = self._token_exchange(TokenType.AUTH_CODE, resp["code"])
            self.cfg.set_opt(c.ACS_TKN, resp[c.ACS_TKN])
            self.cfg.set_opt(c.EXPR_AT, str(resp[c.EXPR_AT]))
            self.cfg.set_opt(c.EXPR_IN, str(resp[c.EXPR_IN]))
            self.cfg.set_opt(c.RFSH_TKN, resp[c.RFSH_TKN])
            self.cfg.write_to_file()

    def _recv_access_resp(self, resp_srv, app):
        try:
            resp_srv.handle_request()
        except KeyboardInterrupt:
            print("Cancelled by user")

        resp_srv.server_close()
        if (resp_srv.access_resp):
            print("Access Granted")
        else:
            print("Access Denied")

        app.end()

    def _request_access(self, scope):
        scope_str = scope.to_str()

        resp_srv = AccessRespServer()
        srv_addr = "http://" + \
            resp_srv.server_address[0] + ":" + str(resp_srv.server_address[1])

        params = {c.CID: self.cfg.cid, c.REDIR_URL: srv_addr,
                  c.RESP_TYP: "code", c.APPR_PROMPT: "auto",
                  c.SCOPE: scope_str}

        access_url = Request("GET", c.ACCESS_URL, params=params).prepare().url

        app = WebApp(access_url)
        Thread(target=self._recv_access_resp, args=(resp_srv, app)).start()
        app.run()

        return resp_srv.access_resp

    def _token_exchange(self, grant_type, token):
        params = {c.CID: self.cfg.cid, c.CSCRT: self.cfg.get_opt(c.CSCRT),
                  c.GRNT_TYP: grant_type.tkn_type,
                  grant_type.param_name: token}
        resp = post(c.TOKEN_URL, params=params)
        if (resp.status_code != 200):
            raise RuntimeError("Token Exchange Failed.\nError Code: %d\n%s" %
                               (resp.status_code, str(resp.json())))

        return resp.json()

    def _update_tkns(self):
        if (int(self.cfg.get_opt(c.EXPR_AT)) - time.time() < 600):
            resp = self._token_exchange(
                TokenType.REFRESH_TKN, self.cfg.get_opt(c.RFSH_TKN))
            self.cfg.set_opt(c.ACS_TKN, resp[c.ACS_TKN])
            self.cfg.set_opt(c.EXPR_AT, str(resp[c.EXPR_AT]))
            self.cfg.set_opt(c.EXPR_IN, str(resp[c.EXPR_IN]))
            self.cfg.set_opt(c.RFSH_TKN, resp[c.RFSH_TKN])
            self.cfg.write_to_file()

    def _get_header_auth(self):
        self._update_tkns()
        return {"Authorization": "Bearer %s" % self.cfg.get_opt(c.ACS_TKN)}
