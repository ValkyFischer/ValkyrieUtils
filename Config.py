#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 01, 2023
@author: v_lky

--------

About:
    This module provides a versatile configuration reader for INI, XML, JSON and VCF files.
    It allows users to easily read and retrieve configuration values from these file formats.
    The supported operations include fetching values as strings, integers, floats, booleans,
    and dictionaries, allowing for flexible usage based on the configuration file type.
    VCF files are encrypted using Argon2 and AES-GCM.
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
        {'Test1': {'order': 1, 'value': 'test_key_xml', 'version': 'test_0.2'}, 'Test2': {'__data__': 'DataXML', 'name': 'test_xml', 'order': 2, 'value': 2000}}
        
        
        >>> config_json = ValkyrieConfig("example.json")
        >>> config_json.get_string("Test1", "value")
        'test_key_json'
        >>> config_json.get_int("Test2", "value")
        3000
        >>> config_json.get_config()
        {'Test1': {'order': 1, 'value': 'test_key_json', 'version': 'test_0.3'}, 'Test2': {'name': 'test_json', 'order': 2, 'value': 3000}}
        
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
    
    example.json:
        {
            "Test1": {
                "value": "test_key_json",
                "version": "test_0.1",
                "order": 1
            },
            "Test2": {
                "value": 3000,
                "name": "test_json",
                "order": 2
            }
        }
        
"""

import configparser
import json
import logging
import pickle
import xml.dom.minidom
import os
from collections import OrderedDict

from Crypto import ValkyrieCrypto, AES_GCM
from Tools import ValkyrieTools


# ===============================


class ValkyrieConfig:
    """
    Initialize a ValkyrieConfig instance based on the file extension.

    Args:
        absolute_path_and_file (str): The absolute path to the configuration file.
            Supported file extensions: .ini, .xml, .json, .vcf
    """
    def __init__(self, absolute_path_and_file, logger: logging.Logger = False, debug: bool = False):
        self.path = absolute_path_and_file
        self.debug = debug
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger("ValkyriePackage")
            self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
            self.logger.addHandler(logging.StreamHandler())
        self.encrypt = False
        self.ext: str
        self.config_handler: IniReader | XmlReader | JsonReader | CryptoReader
        self._detect()
    
    def _detect(self):
        _, extension = os.path.splitext(self.path)
        if extension.lower() == '.ini':
            self.ext = 'ini'
            self.config_handler = IniReader(self.path)
        elif extension.lower() == '.xml':
            self.ext = 'xml'
            self.config_handler = XmlReader(self.path)
        elif extension.lower() == '.json':
            self.ext = 'json'
            self.config_handler = JsonReader(self.path)
        elif extension.lower() == '.vcf':
            self.ext = 'vcf'
            self.config_handler = CryptoReader(self.path)
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
        try:
            return self.config_handler.get_string(section, key, default)
        except Exception as e:
            raise ValueError("Invalid value for key: {}".format(key))
    
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
        try:
            return self.config_handler.get_int(section, key, default)
        except Exception as e:
            raise ValueError("Invalid value for key: {}".format(key))
    
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
        try:
            return self.config_handler.get_boolean(section, key, default)
        except Exception as e:
            raise ValueError("Invalid value for key: {}".format(key))
    
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
        try:
            return self.config_handler.get_float(section, key, default)
        except Exception as e:
            raise ValueError("Invalid value for key: {}".format(key))
    
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
        try:
            config = self.config_handler.get_dict(section)
            return dict(OrderedDict(sorted(config.items(), key=lambda x: x[0])))
        except Exception as e:
            raise ValueError(f"Failed to get configuration data: {e}")
    
    def get_config(self):
        """
        Get the complete configuration as a dictionary.
        
        Returns:
            dict: An ordered dictionary of key-value pairs.
        """
        config_dict = {}
        if self.ext == 'vcf':
            return self.config_handler.json_doc
        elif self.ext == 'ini':
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
        elif self.ext == 'json':
            return self.config_handler.json_doc
        else:
            raise ValueError("Unsupported file format: {}".format(self.ext))
        
    def save(self, config_dict, file = None):
        """
        Save the configuration data to a file.
        
        Args:
            config_dict (dict): The configuration data to save.
            file (str): The file to save the configuration data to.
            
        Returns:
            None
        """
        if file is None:
            file = self.path
        if self.encrypt:
            self.config_handler = CryptoReader(file)
        if self.ext == 'ini' or self.ext == 'xml' or self.ext == 'json' or self.ext == 'vcf':
            self.config_handler.save(config_dict, file)
        else:
            raise ValueError("Unsupported file format: {}".format(self.ext))


# ===============================


class IniReader:
    """
    Initialize a ValkyrieIni instance.

    Args:
        absolute_path_and_file (str): The absolute path to the INI configuration file.
    """
    def __init__(self, absolute_path_and_file):
        self.path = absolute_path_and_file
        self.cp = configparser.RawConfigParser()
        self.cp.read(self.path)
    
    def get_value(self, node, default):
        raise NotImplementedError("This method is not supported for INI files.")
    
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
    
    def save(self, config_dict, file = None):
        if file is None:
            file = self.path
        try:
            with open(file, 'w') as f:
                for key, value in config_dict.items():
                    f.write("[{}]\n".format(key))
                    for k, v in value.items():
                        f.write("{}={}\n".format(k, v))
                    f.write("\n")
            self.__init__(file)
        except Exception as e:
            raise Exception(f"Failed to save configuration data to file: {e}")


class XmlReader:
    """
    Initialize a ValkyrieXml instance.

    Args:
        absolute_path_and_file (str): The absolute path to the XML configuration file.
    """
    def __init__(self, absolute_path_and_file):
        self.path = absolute_path_and_file
        self.xml_doc = xml.dom.minidom.parse(self.path)
    
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
    
    def save(self, config_dict, file = None):
        if file is None:
            file = self.path
        try:
            with open(file, 'w') as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                f.write("<Config>\n")
                for key, value in config_dict.items():
                    f.write("    <{0} ".format(key))
                    __data__ = value.pop('__data__', None)
                    for k, v in value.items():
                        f.write("{0}=\"{1}\" ".format(k, v))
                    if __data__ is None:
                        f.write("/>\n")
                    else:
                        f.write(">{0}</{1}>\n".format(__data__, key))
                f.write("</Config>\n")
            self.__init__(file)
        except Exception as e:
            raise Exception(f"Failed to save configuration data to file: {e}")
        

class JsonReader:
    """
    Initialize a ValkyrieJson instance.

    Args:
        absolute_path_and_file (str): The absolute path to the JSON configuration file.
    """
    def __init__(self, absolute_path_and_file: str):
        self.path = absolute_path_and_file
        self.json_doc = self.__read__()

    def __read__(self):
        """
        Read the JSON configuration file and return the parsed data.

        Returns:
            dict: The parsed configuration data.
        """
        with open(self.path) as file:
            return json.load(file)
    
    def get_value(self, node, default):
        raise NotImplementedError("This method is not supported for JSON files.")
    
    def get_string(self, node, attr, default = None):
        return self._get_raw(node, attr, default).strip("'") if self._get_raw(node, attr, default) else default
    
    def get_int(self, node, attr, default = None):
        return int(self._get_raw(node, attr, default)) if self._get_raw(node, attr, default) else default
    
    def get_boolean(self, node, attr, default = None):
        return self._get_raw(node, attr, default) if self._get_raw(node, attr, default) else default
    
    def get_float(self, node, attr, default = None):
        return float(self._get_raw(node, attr, default)) if self._get_raw(node, attr, default) else default
    
    def _get_raw(self, node, attr, default = None):
        return self.json_doc[node][attr] if node in self.json_doc and attr in self.json_doc[node] else default
    
    def get_dict(self, node):
        return self.json_doc[node] if node in self.json_doc else {}
    
    def save(self, config_dict, file = None):
        if file is None:
            file = self.path
        try:
            with open(file, 'w') as f:
                json.dump(config_dict, f, indent = 4)
            self.__init__(file)
        except Exception as e:
            raise Exception(f"Failed to save configuration data to file: {e}")


class CryptoReader(JsonReader):
    """
    Initialize a CryptoReader instance for reading and writing encrypted configuration files.

    Args:
        absolute_path_and_file (str): The absolute path to the encrypted configuration file.
    """
    def __init__(self, absolute_path_and_file: str):
        super().__init__(absolute_path_and_file)
        self.argon_key: bytes = None
        
    def __read__(self):
        """
        Read encrypted configuration file and return the parsed data.
        
        Returns:
            dict: The decrypted configuration data.
        """
        if os.path.exists(self.path):
            with open(self.path) as file:
                data = file.read()
        
            if not data:
                raise Exception("Cannot read config!")
            
            if self.argon_key is None:
                self.argon_key = ValkyrieCrypto.__key__()
            
            encrypted_data = json.loads(data)
            decrypted_data = ValkyrieCrypto.decrypt_data(self.argon_key, encrypted_data, AES_GCM)
            config = pickle.loads(decrypted_data)
            
        else:
            config = {}
            
        return config
    
    def save(self, config_dict, file = None):
        """
        Save the data in an encrypted configuration file.
        
        Args:
            config_dict (dict): The configuration data to save.
            file (str): The file to save the configuration data to.
        """
        if file is None:
            file = self.path
            
        if self.argon_key is None:
            self.argon_key = ValkyrieCrypto.__key__()
            
        pickled_data = pickle.dumps(config_dict)
        encrypted_data = ValkyrieCrypto.encrypt_data(self.argon_key, pickled_data, AES_GCM)
        
        with open(file, "w") as f:
            f.write(json.dumps(encrypted_data, indent = 4))
            
        self.__init__(file)


# ===============================


if __name__ == '__main__':
    print("Running a test for ValkyrieConfig...")
    # ================================
    print("-" * 50)
    # ================================
    
    # INI file example
    config_reader_ini = ValkyrieConfig("examples/example.ini")
    print(f"File: {config_reader_ini.path}")
    print(config_reader_ini.get_string('Test1', 'test_key1'))  # returns string
    print(config_reader_ini.get_int('Test2', 'test_key2'))  # returns int
    print(config_reader_ini.get_dict('Test1'))  # returns dict
    print(config_reader_ini.get_dict('Test2'))  # returns dict
    print(config_reader_ini.get_config())  # returns dict
    
    # ================================
    print("-" * 50)
    # ================================
    
    # XML file example
    config_reader_xml = ValkyrieConfig("examples/example.xml")
    print(f"File: {config_reader_xml.path}")
    print(config_reader_xml.get_value("Test2"))  # returns TestXML
    print(config_reader_xml.get_string("Test1", "value"))  # returns string
    print(config_reader_xml.get_int("Test2", "value"))  # returns int
    print(config_reader_xml.get_dict("Test1"))  # returns dict
    print(config_reader_xml.get_dict("Test2"))  # returns dict
    print(config_reader_xml.get_config())  # returns dict
    
    # ================================
    print("-" * 50)
    # ================================
    
    # JSON file example
    config_reader = ValkyrieConfig("examples/example.json")
    print(f"File: {config_reader.path}")
    print(config_reader.get_string("Test1", "value"))  # returns string
    print(config_reader.get_int("Test2", "value"))  # returns int
    print(config_reader.get_dict("Test1"))  # returns dict
    print(config_reader.get_dict("Test2"))  # returns dict
    print(config_reader.get_config())  # returns dict
    
    # ================================
    print("-" * 50)
    # ================================
    
    # Save the configuration data to a file
    config_reader_ini.save(config_reader_ini.get_config(), "examples/out/example.ini")
    print(f"File saved: {config_reader_ini.path}")
    config_reader_xml.save(config_reader_xml.get_config(), "examples/out/example.xml")
    print(f"File saved: {config_reader_xml.path}")
    config_reader.save(config_reader.get_config(), "examples/out/example.json")
    print(f"File saved: {config_reader.path}")
    
    # Add new configuration data
    cfg = config_reader.get_config()
    cfg['Test1']['value'] = "test_key_crypto"
    cfg['Test1']['version'] = "test_0.4"
    cfg['Test2']['value'] = 4000
    cfg['Test2']['name'] = "test_crypto"
    # Save the configuration data to an encrypted file
    config_reader.encrypt = True
    config_reader.path = "examples/out/example.vcf"
    config_reader.save(config_reader.get_config())
    print(f"File saved: {config_reader.path}")
    
    # ================================
    print("-" * 50)
    # ================================
    
    # Read the encrypted configuration file
    config_reader = ValkyrieConfig("examples/out/example.vcf")
    print(f"File: {config_reader.path}")
    print(config_reader.get_string("Test1", "value"))  # returns string
    print(config_reader.get_int("Test2", "value"))  # returns int
    print(config_reader.get_dict("Test1"))  # returns dict
    print(config_reader.get_dict("Test2"))  # returns dict
    print(config_reader.get_config())  # returns dict
    
    # ================================
    print("-" * 50)
    # ================================
    