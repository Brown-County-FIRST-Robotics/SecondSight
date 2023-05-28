#!/usr/bin/env python

"""
Secondsight configuration module. This module contains one singleton configuration
class that should be used across the entire system.

The object is a singleton so that if any data is modified, the changes
will be seen by all consumers of configuration data.
"""

import logging
import sys
import json
import os
from typing import Dict, Any

class Configuration(object):
    """
    A singleton class that holds the configuration data for the system.
    This object needs the set_path() to be called before configuration data
    can be read or written to.
    """

    # Setting some defaults makes the initial configuration much easier
    # Remove this eventually
    __default_config = {
        "default": True,
        "cameras": [
            {
                "port": 0,
                "calibration": None,
                "role": "conecube",
                "pos": None
            }
        ],
        "nt_dest": "127.0.0.1",
        "cube_hsv": [150, 138, 121],
        "config_required": True
    }

    variables = None
    file_path = None

    def __new__(cls):
        """
        Only ever create one instance of this class
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
        return cls.instance

    def set_path(self, file_path) -> None:
        """
        Set the file to store the configuration data.
        This method must be called before configuration data can be used
        If the configuration file is not found, some sensible defaults will be used and a
        configuration file will be written

        Parameters:
        file_path (str): The path to a configuarion file

        Returns:
        None
        """
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            self.variables = self.__default_config
            self.write()
            logging.critical('No configuration found')
            logging.critical('Once the server starts, please go to http://localhost:5000/config')
        else:
            with open(self.file_path, 'r') as fh_in:
                self.variables = json.load(fh_in)

    def write(self) -> None:
        """
        Write the current configuration file to disk

        Parameters:
        None

        Returns:
        None
        """

        # If we're saving this, it's not the default config anymore
        if "default" in self.variables:
            del(self.variables["default"])

        with open(self.file_path, 'w') as fh_out:
            json.dump(self.variables, fh_out)

    def close(self) -> None:
        """
        Write the current configuration file to disk and set the
        variables to None preventing further updates without reopening a configuration file.

        Parameters:
        None

        Returns:
        None
        """
        self.write()
        self.variables = None

    def get_all(self) -> Dict[str, Any]:
        """
        Return the entire configuration structure

        Paremeters:
        None

        Returns:
        Any: The full configuration dictionary
        """
        return self.variables

    def get_value(self, item) -> Any:
        """
        Get a configuration value

        Paremeters:
        item (str): The configuration item to lookup and return

        Returns:
        Any: The data stored for that configuration item
        """
        # The fact that this returns Any is possibly a problem
        # Being able to nest configuration data makes it hard to
        # know what you will get back vs making all configuration data
        # Dict[str, str]

        if self.variables is not None and item in self.variables:
            return self.variables[item]
        return None

    def del_value(self, item) -> None:
        """
        Remove a configuration item

        Parameters:
        itemv(str): The key for the configuration item

        Returns:
        None
        """
        self.variables.pop(item)

    def value_exists(self, item) -> bool:
        """
        Check if a configuration item exists in the data

        Parameters:
        itemv(str): The key for the configuration item

        Returns:
        bool:True if value present
        """
        return item in self.variables

    def set_value(self, item, value) -> None:
        """
        Store a configuration value

        Parameters:
        item (str): The key for the configuration item
        value (Any): The configuration data to store

        Returns:
        None
        """
        self.variables[item] = value


if __name__ == "__main__":
    # This file should never be run
    pass
