#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 14:58:13 2022.

@author: Nishad Mandlik
"""

from .config import Cfg
from . import consts as c
from .enums import AccessScope, ActivityFileType, Sport, TokenType
from .enums import ReqType as RT
from .server import AccessRespServer
from .web_view import WebApp
from datetime import datetime as dt
from requests import post, Request, request
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

    def req(self, req_type, url, params=None, data=None, file_path=None):
        """
        Send a request and return the received response.

        Parameters
        ----------
        req_type : PstrYve.ReqType
            Type of the request.
        url : str
            Request URL.
        params : dict, optional
            Query parameters. The default is None.
        data : dict, optional
            Form data. The default is None.
        file_path : pathlib.Path like, optional
            Path of the file to be uploaded. The default is None.

        Returns
        -------
        dict
            Request response.

        """
        self._update_tkns()
        headers = {"Authorization": "Bearer %s" % self.cfg.get_opt(c.ACS_TKN)}
        if (file_path is not None):
            with open(file_path, "r") as f:
                r = request(req_type.label, url, params=params,
                            headers=headers, data=data, file={"file": f})
        else:
            r = request(req_type.label, url, params=params, headers=headers,
                        data=data)

        return r.json()

    def create_manual_activity(self, name, sport_type, start_date_local,
                               elapsed_tm, dist, desc=None, trainer=False,
                               commute=False):
        """
        Create a manual activity for an athlete.

        Refer to 
        https://developers.strava.com/docs/reference/#api-Activities-createActivity

        Parameters
        ----------
        name : str
            Name of the activity.
        sport_type : PstrYve.Sport
            Type of sport.
        start_date_local : str or float or datetime.datetime
            ISO 8601 string or Unix timestamp or datetime object specifying the
            start time of the activity.
        elapsed_tm : int
            Activity duration (in seconds).
        dist : int
            Distance covered (in meters).
        desc : str or None, optional
            Activity description. The default is None.
        trainer : bool, optional
            True if the activity was completed on a trainer, False otherwise.
            The default is False.
        commute : bool, optional
            True if the activity was a commute, False otherwise.
            The default is False.

        Returns
        -------
        dict
            Details of the created activity if successful,
            Error details otherwise.

        """
        if (type(start_date_local) == str):
            date = start_date_local
        elif (type(start_date_local) == float):
            date = dt.fromtimestamp(start_date_local).isoformat()
        elif (type(start_date_local) == dt):
            date = start_date_local.isoformat()

        data = {"name": name, "type": sport_type.flag_name,
                "start_date_local": date, "elapsed_time": elapsed_tm,
                "distance": dist,
                "description": (desc if desc is not None else ""),
                "trainer": int(trainer), "commute": int(commute)}

        resp = self.req(RT.POST, c.ACTV_URL, data=data)
        return resp
