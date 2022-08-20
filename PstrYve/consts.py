#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 04:38:09 2022.

@author: Nishad Mandlik
"""

ACCESS_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/api/v3/oauth/token"
DEAUTH_URL = "https://www.strava.com/oauth/deauthorize"

ACTV_URL = "https://www.strava.com/api/v3/activities"
ATHL_URL = "https://www.strava.com/api/v3/athlete"
CLUB_URL = "https://www.strava.com/api/v3/clubs"
GEAR_URL = "https://www.strava.com/api/v3/gear"
ROUTE_URL = "https://www.strava.com/api/v3/routes"
SEG_URL = "https://www.strava.com/api/v3/segments"
SEG_EFF_URL = "https://www.strava.com/api/v3/segment_efforts"
UPLD_URL = "https://www.strava.com/api/v3/uploads"


# HTTP Parameter Names
CID = "client_id"
CSCRT = "client_secret"
CODE = "code"
RFSH_TKN = "refresh_token"
ACS_TKN = "access_token"
REDIR_URL = "redirect_uri"
RESP_TYP = "response_type"
APPR_PROMPT = "approval_prompt"
SCOPE = "scope"
STATE = "state"
GRNT_TYP = "grant_type"
EXPR_AT = "expires_at"
EXPR_IN = "expires_in"
ATHL = "athlete"
