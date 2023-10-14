#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 01, 2023
@author: v_lky

--------

About:
    This module provides a configurable command-line option parser using OptionParser.
    It allows easy definition of options with specified data types, help messages, and default values.
    The parsed options can be accessed through a dictionary-like interface.
--------

Example:
    >>> options_parser = ValkyrieOptions([
         ('server_id', 'int', 'Server ID'),  # name, type, help - no default
         ('config_file', 'str', 'Configuration File Path and filename', 'valkyrie.conf')  # name, type, help, default
    ])
    >>> parsed = options_parser.parse()
    >>> parsed.keys()
    ['server_id', 'config_file']
    >>> parsed['server_id']
    1
    >>> parsed.config_file
    'valkyrie.conf'

"""

from optparse import OptionParser
import sys


# ===============================


class ValkyrieOptions:
    """
    A class to manage command line options and configuration.

    This class uses OptionParser to handle command line options.

    Args:
        *options: Variable number of tuples representing each option.
            Each tuple should have the format (name, type, help, default_value).
            name (str): The name of the option.
            type (str): The type of the option.
            help (str): The help text for the option.
            default_value (any): The default value for the option.
            
    Example:
        >>> options_parser = ValkyrieOptions([
        ...     ('server_id', 'int', 'Server ID'),  # name, type, help - no default
        ...     ('config_file', 'str', 'Configuration File Path and filename', 'valkyrie.conf')  # name, type, help, default
        ... ])
        >>> parsed = options_parser.parse()
        >>> parsed.keys()
        ['server_id', 'config_file']
        >>> parsed['server_id']
        1
        >>> parsed.config_file
        'valkyrie.conf'
        
    """
    
    def __init__(self, *options):
        self._parser = OptionParser()
        self.add_option(*options)
    
    def add_option(self, *options):
        """
        Add a new option to the parser.
        
        Args:
            *options: Variable number of tuples representing each option.
                Each tuple should have the format (name, type, help, default_value).
                name (str): The name of the option.
                type (str): The type of the option.
                help (str): The help text for the option.
                default_value (any): The default value for the option.
        """
        if len(options) >= 1:
            for option in options[0]:
                name, data_type, help_text = option[:3]
                self._parser.add_option('--' + name, dest = name, type = data_type, help = help_text, default = None if len(option) < 4 else option[3])
    
    def parse(self, args = None):
        """
        Parse the command line arguments.

        Args:
            args (list): A list of command line arguments. Default is sys.argv[1:].

        Returns:
            CmdOptions: A command line option instance with the parsed options.
        """
        if args is None:
            args = sys.argv[1:]
        result = self._parser.parse_args(args)[0].__dict__
        
        if 'config_file' not in result or result['config_file'] is None:
            return CmdOptions(result)
        
        # try:
        #     with open(result['config_file'], 'r') as fp:
        #         for line in fp:
        #             line = line.strip()
        #             print(line)
        #             if line.startswith('[') or line.startswith('#'):
        #                 continue
        #             if '=' in line:
        #                 key, value = line.split('=', 1)
        #             option = self._parser.get_option('--' + key)
        #             if option is None or key in result and result[key] is not None:
        #                 continue
        #             if option.type == 'int':
        #                 result[key] = int(value)
        #             else:
        #                 result[key] = value.strip()
        #
        # except IOError:
        #     pass
        
        return CmdOptions(result)


class CmdOptions(dict):
    """
    A class to manage configuration options.

    This class is a subclass of dict, so you can use it like a dictionary.

    Args:
        options (dict): A dictionary of configuration options.

    Example:
        >>> config = CmdOptions({'server_id': 1, 'wot_ip': '127.0.0.1'})
        >>> config['server_id']
        1
        >>> config.config_file
        'valkyrie.conf'

    """
    
    def __getattr__(self, key):
        return self.get(key)


# ===============================


if __name__ == '__main__':
    # ================================
    print("-" * 50)
    # ================================
    
    # Add options on the fly while initializing
    options_parser = ValkyrieOptions([
        ('server_id',   'int', 'Server ID'),
        ('config_file', 'str', 'Configuration File Path and filename', 'valkyrie.conf')
    ])
    print("Initialised Valkyrie Command Line Options")
    
    # Add options after initializing
    options_parser.add_option([
        ('log_level', 'str', 'Log writing level'),
        ('log_file', 'str', 'Log path(absolute) and file name')
    ])
    print("Added Valkyrie Command Line Options")
    
    # Add options after initializing with a loop
    options = {
        'wot': [
            ('wot_ip', 'str', 'WOT IP Address'),
            ('wot_port', 'int', 'WOT Port'),
        ],
        'db': [
            ('db_host', 'str', 'Host Name of DB'),
            ('db_port', 'int', 'Port Number of DB'),
            ('db_user', 'str', 'User Name of DB'),
            ('db_pass', 'str', 'User Password of DB'),
            ('db_base', 'str', 'Catalog of DB'),
        ]
    }
    for section, options in options.items():
        options_parser.add_option(options)
    print("Added Valkyrie Command Line Options (Loop)")
    
    # Parse the user execution options
    parsed_options = options_parser.parse()
    print("Parsed given Command Line Options")
    
    # Print the parsed options
    print(parsed_options.keys(), parsed_options)
    print(parsed_options['server_id'])
    print(parsed_options.config_file)

    # ================================
    print("-" * 50)
    # ================================
