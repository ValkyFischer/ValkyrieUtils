#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 01, 2023
@author: v_lky

--------

About:
    A script to demonstrate how to use ValkyrieUtils:
        - Logger.py
        - Config.py
        - Tools.py
        - Options.py
        - Compressor.py
        - Crypto.py
--------

Usage:
    `python ValkyrieUtils.py --config_file example.xml`
--------

Example:
    >>> logger = ValkyrieLogger('info', 'log/logger.log', 'ValkyrieUtils', True)
    
    >>> config = ValkyrieConfig('example.ini')
    
    >>> parser = ValkyrieOptions([
    ...    ('config_file', 'str', 'Configuration File Path and filename', 'example.ini'),
    ... ])
    
    >>> compressed_data = ValkyrieCompressor.deflate(b"Sample data to be compressed", 'zstd')
    >>> decompressed_data = ValkyrieCompressor.inflate(compressed_data, 'zstd')
    
    >>> argon_key = ValkyrieCrypto.generate_argon_key('0123456789abcdef0123456789abcdef', '0123456789abcdef')
    >>> encrypted_data = ValkyrieCrypto.encrypt_data(argon_key, b"Sample data to be encrypted")
    >>> decrypted_data = ValkyrieCrypto.decrypt_data(argon_key, encrypted_data)
    
    >>> matched_config = ValkyrieTools.matchDict(config.get_dict("Test1"))

"""

from Logger import ValkyrieLogger
from Config import ValkyrieConfig
from Tools import ValkyrieTools
from Options import ValkyrieOptions
from Compressor import ValkyrieCompressor
from Crypto import ValkyrieCrypto, AES_GCM

import pickle


# ===============================


def save_config_data(conf, file):
    """
    Save the configuration data to a file.
    
    Args:
        conf (dict): The configuration data to save.
        file (str): The file to save the configuration data to.
    """
    with open(file, 'w') as f:
        f.write("| {:<15} | {:<75} |\n".format("KEY", "VALUE"))
        f.write("| {:<15} | {:<75} |\n".format("-"*15, "-"*75))
        for key, value in conf.items():
            if isinstance(value, dict):
                f.write("| {:<15} | {:<75} |\n".format(f"NODE: {key}", ""))
                for k, v in value.items():
                    f.write("| {:<15} | {:<75} |\n".format(k, v))
                f.write("| {:<15} | {:<75} |\n".format("-"*15, "-"*75))
            else:
                f.write("| {:<15} | {:<75} |\n".format(key, value))


def run_test(debug):
    """
    Run a test to demonstrate how to use ValkyrieUtils.
    """
    from os import path, makedirs
    if not path.exists('logs'):
        makedirs('logs')
    
    # Create a new logger instance
    logger = ValkyrieLogger('debug' if debug else 'info', 'logs/logger.log', 'ValkyrieUtils', True, debug)
    logger.Info('Loading a new Valkyrie Utils instance')
    
    # line
    logger.Info('-'*90)
    
    # Initialize the command line options
    parser = ValkyrieOptions([
        ('config_file', 'str', 'Configuration File Path and filename', 'examples/example.ini'),
    ])
    options = parser.parse()
    ext = options.config_file.split('.')[-1]
    logger.Info('Initialized the command line options')
    if debug: logger.Debug(f'Options: {options}')
    
    # Read the configuration file
    config = ValkyrieConfig(f'examples/example.{ext}')
    logger.Info(f'Read example.{ext}')

    # Get the complete configuration as a dictionary
    config_dict = ValkyrieTools.matchDict(config.get_config())
    logger.Info(f'Convert complete configuration to a dictionary')
    if debug: logger.Debug(f'Dict: {config_dict}')
    
    # Get the configuration nodes as a dictionary
    config_dict_1 = ValkyrieTools.matchDict(config.get_dict("Test1"))
    config_dict_2 = ValkyrieTools.matchDict(config.get_dict("Test2"))
    logger.Info('Convert the configurations to a dictionary')
    if debug: logger.Debug(f'Dict: {config_dict_1}')
    if debug: logger.Debug(f'Dict: {config_dict_2}')
    
    # Save the complete configuration to a new file
    save_config_data(config_dict, f'examples/out/Complete_{ext}.conf')
    logger.Info(f'Save the complete "{ext}" configuration to a new file')
    if debug: logger.Debug(f'File: examples/out/Complete_{ext}.conf')
    
    # Save the configuration to a new file
    save_config_data(config_dict_1, f'examples/out/Test1_{ext}.conf')
    save_config_data(config_dict_2, f'examples/out/Test2_{ext}.conf')
    logger.Info(f'Save the "{ext}" configuration to a new files')
    if debug: logger.Debug(f'File: examples/out/Test1_{ext}.conf')
    if debug: logger.Debug(f'File: examples/out/Test2_{ext}.conf')
    
    # Compress the configuration data
    compressed_config = ValkyrieCompressor.deflate(pickle.dumps(config_dict), 'zstd')
    logger.Info(f'Compress the configuration the data')
    if debug: logger.Debug(f'Compressed Data: {compressed_config}')
    
    # Create a new argon encryption key
    argon_key = ValkyrieCrypto.generate_argon_key('0123456789abcdef0123456789abcdef', '0123456789abcdef')
    logger.Info(f'Create a new argon encryption key')
    if debug: logger.Debug(f'Argon Key: {argon_key}')
    
    # Encrypt the compressed configuration data
    encrypted_config = ValkyrieCrypto.encrypt_data(argon_key, compressed_config, AES_GCM)
    logger.Info(f'Encrypt the compressed configuration data')
    if debug: logger.Debug(f'Encrypted Data: {encrypted_config}')
    
    # Decrypt the ciphertext
    decryption_config = ValkyrieCrypto.decrypt_data(argon_key, encrypted_config, AES_GCM)
    logger.Info(f'Decrypt the compressed configuration data')
    if debug: logger.Debug(f'Decrypted Data: {decryption_config}')
    
    # Decompress the configuration data
    decompressed_config = pickle.loads(ValkyrieCompressor.inflate(decryption_config, 'zstd'))
    logger.Info(f'Decompress the configuration the data')
    if debug: logger.Debug(f'Decompressed Data: {decompressed_config}')
    
    # line
    if debug: logger.Info('-'*90)
    
    # Print the data sizes
    if debug: logger.Debug(f'Compressed Size   : {len(compressed_config)} bytes')
    if debug: logger.Debug(f'Decompressed Size : {len(pickle.dumps(decompressed_config))} bytes')
    if debug: logger.Debug(f'Encrypted Size    : {len(pickle.dumps(encrypted_config))} bytes')
    if debug: logger.Debug(f'Decrypted Size    : {len(decryption_config)} bytes')
    
    # line
    logger.Info('-'*90)


# ===============================


if __name__ == '__main__':
    run_test(debug=False)
