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
        
    Returns:
        None
    """
    try:
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
                    
    except Exception as e:
        raise Exception(f"Failed to save configuration data to file: {e}")


def run_test(debug):
    """
    Run a test to demonstrate how to use ValkyrieUtils.
    
    Args:
        debug (bool): Enable debug mode.
        
    Returns:
        None
    """
    from os import path, makedirs
    if not path.exists('logs'):
        makedirs('logs')
    
    # Create a new logger instance
    logger = ValkyrieLogger('debug' if debug else 'info', 'logs/logger.log', 'ValkyrieUtils', True, debug)
    logger.info('Loading a new Valkyrie Utils instance')
    
    # line
    logger.info('-' * 90)
    
    # Initialize the command line options
    parser = ValkyrieOptions([
        ('config_file', 'str', 'Configuration File Path and filename', 'examples/example.ini'),
    ])
    options = parser.parse()
    ext = options.config_file.split('.')[-1]
    logger.info('Initialized the command line options')
    if debug: logger.debug(f'Options: {options}')
    
    # Read the configuration file
    config = ValkyrieConfig(f'examples/example.{ext}')
    logger.info(f'Read example.{ext}')

    # Get the complete configuration as a dictionary
    config_dict = ValkyrieTools.matchDict(config.get_config())
    logger.info(f'Convert complete configuration to a dictionary')
    if debug: logger.debug(f'Dict: {config_dict}')
    
    # Get the configuration nodes as a dictionary
    config_dict_1 = ValkyrieTools.matchDict(config.get_dict("Test1"))
    config_dict_2 = ValkyrieTools.matchDict(config.get_dict("Test2"))
    logger.info('Convert the configurations to a dictionary')
    if debug: logger.debug(f'Dict: {config_dict_1}')
    if debug: logger.debug(f'Dict: {config_dict_2}')
    
    # Save the complete configuration to a new file
    save_config_data(config_dict, f'examples/out/Complete_{ext}.conf')
    logger.info(f'Save the complete "{ext}" configuration to a new file')
    if debug: logger.debug(f'File: examples/out/Complete_{ext}.conf')
    
    # Save the configuration to a new file
    save_config_data(config_dict_1, f'examples/out/Test1_{ext}.conf')
    save_config_data(config_dict_2, f'examples/out/Test2_{ext}.conf')
    logger.info(f'Save the "{ext}" configuration to a new files')
    if debug: logger.debug(f'File: examples/out/Test1_{ext}.conf')
    if debug: logger.debug(f'File: examples/out/Test2_{ext}.conf')
    
    # Compress the configuration data
    compressed_config = ValkyrieCompressor.deflate(pickle.dumps(config_dict), 'zstd')
    logger.info(f'Compress the configuration the data')
    if debug: logger.debug(f'Compressed Data: {compressed_config}')
    
    # Create a new argon encryption key
    _key = ValkyrieTools.generateCode(64)
    _iv = ValkyrieTools.generateCode(24)
    argon_key = ValkyrieCrypto.generate_argon_key(_key, _iv)
    logger.info(f'Create a new argon encryption key')
    if debug: logger.debug(f'Crypto Key: {_key}')
    if debug: logger.debug(f'Crypto IV: {_iv}')
    if debug: logger.debug(f'Argon Key: {argon_key}')
    
    # Encrypt the compressed configuration data
    encrypted_config = ValkyrieCrypto.encrypt_data(argon_key, compressed_config, AES_GCM)
    logger.info(f'Encrypt the compressed configuration data')
    if debug: logger.debug(f'Encrypted Data: {encrypted_config}')
    
    # Decrypt the ciphertext
    decryption_config = ValkyrieCrypto.decrypt_data(argon_key, encrypted_config, AES_GCM)
    logger.info(f'Decrypt the compressed configuration data')
    if debug: logger.debug(f'Decrypted Data: {decryption_config}')
    
    # Decompress the configuration data
    decompressed_config = pickle.loads(ValkyrieCompressor.inflate(decryption_config, 'zstd'))
    logger.info(f'Decompress the configuration the data')
    if debug: logger.debug(f'Decompressed Data: {decompressed_config}')
    
    # print debug data
    if debug: logger.info('-' * 90)
    if debug: logger.debug(f'Compressed Size   : {ValkyrieTools.formatSize(len(compressed_config))}')
    if debug: logger.debug(f'Decompressed Size : {ValkyrieTools.formatSize(len(pickle.dumps(decompressed_config)))}')
    if debug: logger.debug(f'Encrypted Size    : {ValkyrieTools.formatSize(len(pickle.dumps(encrypted_config)))}')
    if debug: logger.debug(f'Decrypted Size    : {ValkyrieTools.formatSize(len(decryption_config))}')
    
    # line
    logger.info('-' * 90)


# ===============================


if __name__ == '__main__':
    run_test(debug=False)
