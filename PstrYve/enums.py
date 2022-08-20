#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 04:17:28 2022.

@author: Nishad Mandlik
"""

from . import consts as c
from enum import IntFlag, IntEnum


class AutoFlag(IntFlag):
    """Flag Enum with auto value generation."""

    def __new__(cls, flag_name):
        """
        Create new element in the Flag-Enum with the given flag-name.

        Parameters
        ----------
        flag_name : str
            Flag name.

        Returns
        -------
        obj : instance of AutoFlag
            New Flag Enum element.

        """
        val = 2 ** len(cls.__members__)
        obj = int.__new__(cls, val)
        obj._value_ = val
        obj.flag_name = flag_name
        return obj

    def __str__(self):
        """
        Return the string representation of the flag.

        Returns
        -------
        str
            Name of the flag.

        """
        return self.flag_name


class AutoEnum(IntEnum):
    """Enum with auto value generation."""

    def __new__(cls, label):
        """
        Create new element in the Enum with the given label.

        Parameters
        ----------
        label : str
            Name of the type of activity-file.

        Returns
        -------
        obj : ActivityFileType
            New Enum element.

        """
        val = len(cls.__members__)
        obj = int.__new__(cls, val)
        obj._value_ = val
        obj.label = label
        return obj

    def __str__(self):
        """
        Return the string representation for the Enum item.

        Returns
        -------
        str
            Label of the item.

        """
        return self.label


class AccessScope(AutoFlag):
    """
    Flag Enum for Scope of the Requested Access.

    Obtained from https://developers.strava.com/docs/authentication/
    """

    READ = "read"
    READ_ALL = "read_all"
    PROFILE_READ_ALL = "profile:read_all"
    PROFILE_WRITE = "profile:write"
    ACTIVITY_READ = "activity:read"
    ACTIVITY_READ_ALL = "activity:read_all"
    ACTIVITY_WRITE = "activity:write"

    def to_str(self):
        """
        Return the scope as a string.

        Returns
        -------
        scope_str : str
            Comma separated names of set scope-flags.

        """
        scope_list = []
        for flag in self.__class__:
            if (flag & self):
                scope_list.append(flag.flag_name)
        scope_str = ",".join(scope_list)
        return scope_str

    @classmethod
    def from_str(cls, scope_str):
        """
        Create an access-scope object from a string containing flag names.

        Parameters
        ----------
        scope_str : str
            Comma separated names of scope-flags.

        Returns
        -------
        scope : AccessScope
            Bitwise OR-ed flags defining the access-scope.

        """
        scope_str_list = scope_str.split(",")
        scope = 0
        for flag_name in scope_str_list:
            for flag in cls:
                if (flag_name == flag.flag_name):
                    scope = scope | flag
                    break
        return scope

    def check_flags(self, flags):
        """
        Check if the currently set flags are set in the provided flags.

        Parameters
        ----------
        flags : AccessScope or str or None
            Flags to be matched with self.

        Note
        ----
        This function only checks the availability of current flags in the
        provided variable, and not vice-verse. If the provided variable
        contains all of the current flags and also some extra ones, the
        function will return True.

        Returns
        -------
        bool
            True if flags are matched, Flase otherwise.

        """
        if (flags is None):
            flags = 0
        elif (type(flags) == str):
            flags = self.from_str(flags)
        return not bool(self & (~flags))


class Sport(AutoFlag):
    """
    Flag Enum for Scope of the Sport Types.

    Obtained from
    https://developers.strava.com/docs/reference/#api-models-SportType
    """

    E_BIKING = "EBikeRide"
    V_BIKING = "VirtualRide"
    BIKING = "Ride"
    GRAVEL_BIKING = "GravelRide"
    E_MT_BIKING = "EMountainBikeRide"
    MT_BIKING = "MountainBikeRide"
    VELO_MOBILE = "Velomobile"
    HAND_CYCLING = "Handcycle"
    WALKING = "Walk"
    V_RUNNING = "VirtualRun"
    RUNNING = "Run"
    TRAIL_RUNNING = "TrailRun"
    HIKING = "Hike"
    CROSSFIT = "Crossfit"
    ELLIPTICAL = "Elliptical"
    STAIR_STEPPING = "StairStepper"
    CANOEING = "Canoeing"
    ROWING = "Rowing"
    KAYAKING = "Kayaking"
    SAILING = "Sail"
    STANDUP_PADDLING = "StandUpPaddling"
    SURFING = "Surfing"
    KITE_SURFING = "Kitesurf"
    WIND_SURFING = "Windsurf"
    SWIMMING = "Swim"
    ICE_SKATING = "IceSkate"
    INLINE_SKATING = "InlineSkate"
    SKATEBOARDING = "Skateboard"
    ROLLER_SKIING = "RollerSki"
    ALPINE_SKIING = "AlpineSki"
    NORDIC_SKIING = "NordicSki"
    BACKCNTRY_SKIING = "BackcountrySki"
    SNOWBOARDING = "Snowboard"
    SNOWSHOEING = "Snowshoe"
    GOLF = "Golf"
    SOCCER = "Soccer"
    ROCK_CLIMBING = "RockClimbing"
    WEIGHT_TRAINING = "WeightTraining"
    WHEEL_CHAIR = "Wheelchair"
    WORKOUT = "Workout"
    YOGA = "Yoga"


class TokenType(IntEnum):
    """
    Enum for Token Grant Type (Auth Code or Refresh Token).

    Obtained from https://developers.strava.com/docs/authentication/
    """

    def __new__(cls, tkn_type, param_name=None):
        """
        Create new element in the Enum.

        Parameters
        ----------
        tkn_type : str
            Type of the token to be used for authentication.
        param_name : str or None, optional
            Parameter name to be used for the token in the request.
            If None, this is same as 'token_type'. The default is None.

        Returns
        -------
        obj : TokenType
            New Enum element.

        """
        val = len(cls.__members__)
        obj = int.__new__(cls, val)
        obj._value_ = val
        obj.tkn_type = tkn_type
        if param_name is None:
            param_name = tkn_type
        obj.param_name = param_name
        return obj

    AUTH_CODE = ("authorization_code", c.CODE)
    REFRESH_TKN = c.RFSH_TKN


class ActivityFileType(AutoEnum):
    """
    Enum for Activity File Type.

    Obtained from
    https://developers.strava.com/docs/reference/#api-Uploads-createUpload
    """

    FIT = "fit"
    FIT_GZ = "fit.gz"
    TCX = "tcx"
    TCX_GZ = "tcx.gz"
    GPX = "gpx"
    GPX_GZ = "gpx.gz"


class ReqType(AutoEnum):
    """Enum for HTTP Request Type."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
