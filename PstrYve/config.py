#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 03:12:01 2022.

@author: Nishad Mandlik
"""

from configparser import ConfigParser
from pathlib import Path

_CFG_FILE_PATH = Path.home() / ".pstryverc"


class Cfg(ConfigParser):
    def __init__(self, client_id):
        super().__init__()
        self.cid = client_id
        if (not _CFG_FILE_PATH.is_file()):
            open(_CFG_FILE_PATH, 'w').close()
        self.read(_CFG_FILE_PATH)
        if (not self.has_section(self.cid)):
            self.add_section(self.cid)

    def has_opt(self, option):
        """
        Check if the option exists in the client-id config.

        Parameters
        ----------
        option : str
            Option to be checked.

        Returns
        -------
        bool
            True if the option exists, False otherwise.

        """
        return super().has_option(self.cid, option)

    def get_opt(self, option):
        """
        Get the requested option from the client-id config.

        Parameters
        ----------
        option : str
            Option name.

        Returns
        -------
        str or None
            Option value if the option exists, None otherwise.

        """
        return super().get(self.cid, option, fallback=None)

    def set_opt(self, option, val):
        """
        Set the value of the given option in the client-id config.

        Parameters
        ----------
        option : str
            Option name.
        val : str
            Value to be set for the specified option.

        Returns
        -------
        None

        """
        super().set(self.cid, option, val)

    def write_to_file(self):
        """
        Write the current config to the file.

        Returns
        -------
        None.

        """
        with open(_CFG_FILE_PATH, "w") as f:
            self.write(f)
