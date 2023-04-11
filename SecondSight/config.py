#!/usr/bin/env python

import sys
import json

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
    
    def set_path(self, file_path):
        """
        Set the file to store the configuration data.
        This method must be called before configuration data can be used
        """
        self.file_path = file_path
        with open(self.file_path, 'r') as fh_in:
            self.variables = json.load(fh_in)

    def write(self):
        """
        Write the current configuration file to disk
        """
        with open(self.file_path, 'w') as fh_out:
            json.dump(self.variables, fh_out)

    def close(self):
        """
        Write the current configuration file to disk and set the
        variables to None preventing further updates without reopening a configuration file.
        """
        self.write()
        self.variables = None

    def get_value(self, item):
        """
        Get a configuration value
        """
        return self.variables[item]

    def set_value(self, item, value):
        """
        Store a configuration value
        """
        self.variables[item] = value


if __name__ == "__main__":
    # This file should never be run
    pass