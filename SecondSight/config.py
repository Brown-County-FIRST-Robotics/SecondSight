#!/usr/bin/env python
import logging
import sys
import json
import os
from SecondSight.utils import LogMe


class Configuration(object):
    """
    A singleton class that holds the configuration data for the system.
    This object needs the set_path() to be called before configuration data
    can be read or written to
    """

    variables = None
    file_path = None

    def __new__(cls):
        """
        Only ever create one instance of this class
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
        return cls.instance

    @LogMe
    def set_path(self, file_path):
        """
        Set the file to store the configuration data.
        This method must be called before configuration data can be used
        If the configuration file is not found, some sensible defaults will be used and a
        configuration file will be written
        """
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            self.variables = {}
            self.write()
            logging.critical('No configuration found')
            logging.critical('Once the server starts, please go to http://localhost:5000/config')
        else:
            with open(self.file_path, 'r') as fh_in:
                self.variables = json.load(fh_in)

    @LogMe
    def write(self):
        """
        Write the current configuration file to disk
        """
        with open(self.file_path, 'w') as fh_out:
            json.dump(self.variables, fh_out)

    @LogMe
    def close(self):
        """
        Write the current configuration file to disk and set the
        variables to None preventing further updates without reopening a configuration file.
        """
        self.write()
        self.variables = None

    @LogMe
    def get_value(self, item):
        """
        Get a configuration value
        """
        if self.variables is not None and item in self.variables:
            return self.variables[item]
        return None

    @LogMe
    def del_value(self, item):
        self.variables.pop(item)

    @LogMe
    def value_exists(self, item):
        return item in self.variables

    @LogMe
    def set_value(self, item, value):
        """
        Store a configuration value
        """
        self.variables[item] = value

    @LogMe
    def stringify(self):
        return str(self.variables)


if __name__ == "__main__":
    # This file should never be run
    pass
