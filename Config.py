#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 01, 2023
@author: v_lky

--------

About:
    This module provides a versatile configuration reader for INI and XML files.
    It allows users to easily read and retrieve configuration values from these file formats.
    The supported operations include fetching values as strings, integers, floats, booleans,
    and dictionaries, allowing for flexible usage based on the configuration file type.
--------

Example:
        >>> config_ini = ValkyrieConfig("example.ini")
        >>> config_ini.get_string('Test1', 'value')
        'test_key_value'
        >>> config_ini.get_int('Test2', 'value')
        1000
        >>> config_ini.get_config()
        {'Test1': {'order': 1, 'value': 'test_key_ini', 'version': 'test_0.1'}, 'Test2': {'name': 'test_ini', 'order': 2, 'value': 1000}}


        >>> config_xml = ValkyrieConfig("example.xml")
        >>> config_xml.get_string("Test1", "value")
        'test_key_xml'
        >>> config_xml.get_int("Test2", "value")
        2000
        >>> config_xml.get_config()
        {'Test1': {'order': 1, 'value': 'test_key_xml', 'version': 'test_0.1'}, 'Test2': {'__data__': 'DataXML', 'name': 'test_xml', 'order': 2, 'value': 2000}}
--------

Samples:
    example.ini:
        [Test1]
        value=test_key_ini
        version=test_0.1
        order=1
        
        [Test2]
        value=1000
        name=test_ini
        order=2
    
    example.xml:
        <?xml version="1.0" encoding="UTF-8"?>
        <Config>
            <Test1 version="test_0.1" order="1" value="test_key_xml" />
            <Test2 name="test_xml" order="2" value="2000">DataXML</Test2>
        </Config>
        
"""

import configparser
import xml.dom.minidom
import os
from collections import OrderedDict


# ===============================


class ValkyrieConfig:
    """
    Initialize a ValkyrieConfig instance based on the file extension.

    Args:
        absolute_path_and_file (str): The absolute path to the configuration file.
            Supported file extensions: .ini, .xml

    Raises:
        ValueError: If the file format is unsupported.
    """
    def __init__(self, absolute_path_and_file):
        _, extension = os.path.splitext(absolute_path_and_file)
        
        if extension.lower() == '.ini':
            self.ext = 'ini'
            self.config_handler = ValkyrieIniReader(absolute_path_and_file)
        elif extension.lower() == '.xml':
            self.ext = 'xml'
            self.config_handler = ValkyrieXmlReader(absolute_path_and_file)
        else:
            raise ValueError("Unsupported file format: {}".format(extension))
    
    def get_string(self, section, key, default = None):
        """
        Get a string value from the configuration.

        Args:
            section (str): The section to look for.
            key (str, optional): The key to retrieve. Default is None.
            default: The default value to return if the key is not found. Default is None.

        Returns:
            str: The string value.
        """
        return self.config_handler.get_string(section, key, default)
    
    def get_int(self, section, key, default = None):
        """
        Get an integer value from the configuration.

        Args:
            section (str): The section to look for.
            key (str, optional): The key to retrieve. Default is None.
            default: The default value to return if the key is not found. Default is None.

        Returns:
            int: The integer value.
        """
        return self.config_handler.get_int(section, key, default)
    
    def get_boolean(self, section, key, default = None):
        """
        Get a boolean value from the configuration.
    
        Args:
            section (str): The section to look for.
            key (str, optional): The key to retrieve. Default is None.
            default: The default value to return if the key is not found. Default is None.
    
        Returns:
            bool: The boolean value.
        """
        return self.config_handler.get_boolean(section, key, default)
    
    def get_float(self, section, key, default = None):
        """
        Get a float value from the configuration.

        Args:
            section (str): The section to look for.
            key (str, optional): The key to retrieve. Default is None.
            default: The default value to return if the key is not found. Default is None.

        Returns:
            float: The float value.
        """
        return self.config_handler.get_float(section, key, default)
    
    def get_value(self, node, default = None):
        """
        Get a value from the configuration.
        
        Args:
            node (str): The node to look for.
            default: The default value to return if the node is not found. Default is None.
            
        Returns:
            str: The value.
        """
        if self.ext == 'xml':
            return self.config_handler.get_value(node, default)
        else:
            raise ValueError("Unsupported file format: {}".format(self.ext))
    
    def get_dict(self, section):
        """
        Get a full section as a dictionary from the configuration.
        
        Args:
            section (str): The section to look for.
            
        Returns:
            dict: An ordered dictionary of key-value pairs, sorted by keys.
        """
        config = self.config_handler.get_dict(section)
        return dict(OrderedDict(sorted(config.items(), key=lambda x: x[0])))
    
    def get_config(self):
        """
        Get the complete configuration as a dictionary.
        
        Returns:
            dict: An ordered dictionary of key-value pairs.
        """
        config_dict = {}
        if self.ext == 'ini':
            config_node = self.config_handler.cp
            for section in config_node.sections():
                config_dict[section] = self.get_dict(section)
            return config_dict
        elif self.ext == 'xml':
            config_node = self.config_handler.xml_doc.getElementsByTagName('Config')[0]
            for node in config_node.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    config_dict[node.nodeName] = self.get_dict(node.nodeName)
            return config_dict
        else:
            raise ValueError("Unsupported file format: {}".format(self.ext))


# ===============================


class ValkyrieIniReader:
    """
    Initialize a ValkyrieIni instance.

    Args:
        absolute_path_and_file (str): The absolute path to the INI configuration file.
    """
    def __init__(self, absolute_path_and_file):
        self.cp = configparser.RawConfigParser()
        self.cp.read(absolute_path_and_file)
    
    def get_string(self, section, key, default = None):
        return self._get_raw(section, key, default).strip("'") if self._get_raw(section, key, default) else default
    
    def get_int(self, section, key, default = None):
        return int(self._get_raw(section, key, default)) if self._get_raw(section, key, default) else default
    
    def get_boolean(self, section, key, default = None):
        return self.cp.getboolean(section, key) if self._get_raw(section, key, default) else default
    
    def get_float(self, section, key, default = None):
        return float(self._get_raw(section, key, default)) if self._get_raw(section, key, default) else default
    
    def _get_raw(self, section, key, default = None):
        return self.cp.get(section, key, fallback = default)
    
    def get_dict(self, section):
        return dict(self.cp.items(section))


class ValkyrieXmlReader:
    """
    Initialize a ValkyrieXml instance.

    Args:
        absolute_path_and_file (str): The absolute path to the XML configuration file.
    """
    def __init__(self, absolute_path_and_file):
        self.xml_doc = xml.dom.minidom.parse(absolute_path_and_file)
    
    def get_value(self, node, default = None):
        if isinstance(node, str):
            node = self.xml_doc.getElementsByTagName(node)[0]
        return node.firstChild.data if node.firstChild else default
    
    def get_string(self, node, attr, default = None):
        return self._get_raw(node, attr, default).strip("'") if self._get_raw(node, attr, default) else default
    
    def get_int(self, node, attr, default = None):
        return int(self._get_raw(node, attr, default)) if self._get_raw(node, attr, default) else default
    
    def get_boolean(self, node, attr, default = None):
        return self._get_raw(node, attr, default) if self._get_raw(node, attr, default) else default
    
    def get_float(self, node, attr, default = None):
        return float(self._get_raw(node, attr, default)) if self._get_raw(node, attr, default) else default
    
    def _get_raw(self, node, attr, default = None):
        node = self.xml_doc.getElementsByTagName(node)[0]
        return node.getAttribute(attr) if node else default
    
    def get_dict(self, node):
        node = self.xml_doc.getElementsByTagName(node)[0]
        config_dict = {}
        if node:
            config_dict = dict(node.attributes.items())
        if self.get_value(node) is not None:
            config_dict['__data__'] = self.get_value(node)
        return config_dict


# ===============================


if __name__ == '__main__':
    # INI file example
    config_reader_ini = ValkyrieConfig("examples/example.ini")
    print(config_reader_ini.get_string('Test1', 'test_key1'))  # returns string
    print(config_reader_ini.get_int('Test2', 'test_key2'))  # returns int
    print(config_reader_ini.get_dict('Test1'))  # returns dict
    print(config_reader_ini.get_dict('Test2'))  # returns dict
    
    # XML file example
    config_reader_xml = ValkyrieConfig("examples/example.xml")
    print(config_reader_xml.get_string("Test1", "value"))  # returns string
    print(config_reader_xml.get_int("Test2", "value"))  # returns int
    print(config_reader_xml.get_dict("Test1"))  # returns dict
    print(config_reader_xml.get_dict("Test2"))  # returns dict
    print(config_reader_xml.get_value("Test1"))  # returns None
    print(config_reader_xml.get_value("Test2"))  # returns TestXML
    