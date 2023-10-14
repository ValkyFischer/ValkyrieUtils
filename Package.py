#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 03, 2023
@author: v_lky
"""

import logging
import pickle
import struct
import time

try:
    from .Compressor import ValkyrieCompressor
    from .Crypto import ValkyrieCrypto, MODES_D
    from .Tools import ValkyrieTools
    from .Exceptions import *
except ImportError:
    from Compressor import ValkyrieCompressor
    from Crypto import ValkyrieCrypto, MODES_D
    from Tools import ValkyrieTools
    from Exceptions import *


class ValkyriePackage:
    
    def __init__(self, argon_key: bytes, logger: logging.Logger = False, debug: bool = False):
        self.header = '16s22sI16s17sI7sII5s'
        self.version = 2
        self.compression = "zstd"
        self.encryption = "AES-GCM"
        self.author = "Valky Fischer"
        self.argon_key = argon_key
        self.debug = debug
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger("ValkyriePackage")
            self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
            self.logger.addHandler(logging.StreamHandler())
    
    def info(self, vpk_path):
        """
        Get info about VPK files.
        
        Args:
            vpk_path (str): The path to the VPK file.
            is_binary (bool): Read the file in binary mode.
            
        Returns:
            dict: A dictionary with the following keys:
            
                - filename (str): The filename of the VPK file.
                - fileinfo (str): The fileinfo of the VPK file.
                - filesize (int): The filesize of the VPK file.
                - author (str): The author of the VPK file.
                - copyright (str): The copyright message of the VPK file.
                - timestamp (int): The timestamp of the VPK file.
                - encryption (str): The encryption mode of the VPK file.
                - key_length (int): The key length of the VPK file.
                - version (int): The version of the VPK file.
                - compression (str): The compression mode of the VPK file.
        """
        with open(vpk_path, 'rb') as file:
            header_data = file.read(struct.calcsize(self.header))
            head = struct.unpack(self.header, header_data)
        
        header = {
            "filename": head[0].decode().rstrip('\x00'),
            "fileinfo": head[1].decode().rstrip('\x00'),
            "filesize": head[2],
            "author": head[3].decode().rstrip('\x00'),
            "copyright": head[4].decode().rstrip('\x00'),
            "timestamp": head[5],
            "encryption": head[6].decode().rstrip('\x00'),
            "key_length": head[7],
            "version": head[8],
            "compression": head[9].decode().rstrip('\x00')
        }
        
        return header
    
    def read(self, vpk_path: str) -> dict:
        """
        Read a VPK package and return the decrypted data.

        Args:
            vpk_path (str): The path to the VPK file.

        Returns:
            dict: A dictionary with the decrypted data.
        """
        if not self._check(vpk_path):
            return False
        
        compressed_data = self._read_vpk(vpk_path)
        encrypted_data = self._decompress(compressed_data)
        decrypted_data = self._decrypt(encrypted_data)
        
        return decrypted_data
    
    def create(self, dir_path: str, vpk_path: str = False) -> str:
        """
        Create a VPK package from a directory and return the path to the VPK package.
        
        Args:
            dir_path (str): The path to the directory to be packed.
            vpk_path (str): The path where the VPK package should be saved. If not specified, the VPK package will be saved in the same directory as the chosen directory with the same name.
            
        Raises:
            VpkError: If an error occurred while creating the VPK package.
            
        Returns:
            str: The path to the VPK package.
        """
        if not vpk_path:
            vpk_name = dir_path.split("/")[-1] if dir_path not in ["/", "", ".", "./", "\\", ".\\"] else "ValkyrieUtils"
            vpk_path = f"{dir_path}/{vpk_name}.vpk"
            
        byte_dict = self._read_dir(dir_path)
        vpk = self.save(byte_dict, vpk_path)
        
        return vpk
    
    def save(self, byte_dict: dict, vpk_path: str):
        """
        Create a VPK package from a dictionary and return the path to the VPK package.
        
        Args:
            byte_dict (dict): The unencrypted data to save.
            vpk_path (str): The path where the VPK package should be saved. If not specified, the VPK package will be saved in the same directory as the chosen directory with the same name.
            
        Raises:
            VpkError: If an error occurred while creating the VPK package.
            
        Returns:
            str: The path to the VPK package.
        """
        encrypted_data = self._encrypt(byte_dict)
        header_data = self._create_header(vpk_path, encrypted_data)
        compressed = self._compress(encrypted_data)
        vpk = self._save(header_data, compressed, vpk_path)
        
        return vpk
    
    def update(self, byte_dict: dict, vpk_path: str) -> str:
        """
        Update an existing VPK package and return the path to the updated VPK package.
        
        Args:
            vpk_path (str): The path to the VPK file.
            byte_dict (dict): The data to update.
            
        Raises:
            VpkError: If an error occurred while updating the VPK package.
            
        Returns:
            str: The path to the VPK package.
        """
        decrypted_data = self.read(vpk_path)
        decrypted_data.update(byte_dict)
        vpk = self.save(decrypted_data, vpk_path)
        
        return vpk
    
    def _decompress(self, compressed_data: bytes) -> bytes:
        """
        Decompress the VPK package using the specified compression mode.
        
        Args:
             compressed_data (bytes): The compressed data of the VPK package.
             
        Raises:
            CompressorError: If the VPK package is not correctly compressed.
            
        Returns:
            bytes: The decompressed, encrypted data of the VPK package.
        """
        try:
            return ValkyrieCompressor.inflate(compressed_data, self.compression)
        
        except Exception as e:
            self.logger.error(f"An error occurred while decompressing the VPK package:", e)
            raise CompressorError("An error occurred while decompressing the VPK package.")
    
    def _compress(self, encrypted_data: bytes) -> bytes:
        """
        Compress the VPK package using the specified compression mode.
        
        Args:
            header_data (bytes): The header data of the VPK package.
            encrypted_data (bytes): The encrypted data of the VPK package.
            
        Raises:
            CompressorError: If the VPK package is not correctly compressed.
            
        Returns:
            bytes: The compressed data of the VPK package.
        """
        try:
            return ValkyrieCompressor.deflate(encrypted_data, self.compression)
        
        except Exception as e:
            self.logger.error(f"An error occurred while compressing the VPK package:", e)
            raise CompressorError("An error occurred while compressing the VPK package.")
    
    def _decrypt(self, encrypted_data: bytes) -> dict:
        """
        Decrypt the VPK package.
        
        Args:
            encrypted_data (bytes): The encrypted data of the VPK package.
            
        Raises:
            EncryptionError: If the VPK package is not correctly encrypted.
        
        Returns:
            dict: A dictionary with the decrypted data.
        """
        try:
            decrypted_data_bytes = pickle.loads(encrypted_data)
            decrypted_data = ValkyrieCrypto.decrypt_data(self.argon_key, decrypted_data_bytes, mode = MODES_D[self.encryption])
            byte_dict = pickle.loads(decrypted_data)
            return byte_dict
        
        except Exception as e:
            self.logger.error(f"An error occurred while decrypting the VPK package:", e)
            raise DecryptionError("An error occurred while decrypting the VPK package.")
    
    def _encrypt(self, byte_dict: dict) -> bytes:
        """
        Encrypt the VPK package.
        
        Args:
            byte_dict (dict): The data to encrypt.
            
        Raises:
            EncryptionError: If the VPK package is not correctly encrypted.
        
        Returns:
            bytes: The encrypted data of the VPK package.
        """
        try:
            pickled_data = pickle.dumps(byte_dict)
            encrypted_data = ValkyrieCrypto.encrypt_data(self.argon_key, pickled_data, mode = MODES_D[self.encryption])
            encrypted_data_bytes = pickle.dumps(encrypted_data)
            return encrypted_data_bytes
        
        except Exception as e:
            self.logger.error(f"An error occurred while encrypting the VPK package:", e)
            raise EncryptionError("An error occurred while encrypting the VPK package.")

    def _check(self, vpk_path: str) -> bool:
        """
        Check if the VPK package is correctly encrypted, compressed and compatible with this version of Valkyrie Utils.
        
        Args:
            vpk_path (str): The path to the VPK file.
            
        Raises:
            EncryptionError: If the VPK package is not correctly encrypted.
            VersionError: If the VPK package is not compatible with this version of Valkyrie Utils.
            CompressorError: If the VPK package is not correctly compressed.
        """
        head = self.info(vpk_path)
        
        if head['encryption'] != self.encryption:
            self.logger.error("The VPK package is not correctly encrypted.")
            raise EncryptionError
        
        if head['version'] != self.version:
            self.logger.warning(f"The VPK package is not compatible with this version of Valkyrie Utils: {head['filename']}")
        
        if head['compression'] != self.compression:
            self.logger.error("The VPK package is not correctly compressed.")
            raise CompressorError
        
        return True
    
    def _read_vpk(self, vpk_path: str) -> dict:
        """
        Read a VPK package and return the compressed data.
        
        Args:
            vpk_path (str): The path to the VPK file.
            
        Raises:
            VpkError: If an error occurred while reading the VPK package.
        """
        try:
            with open(vpk_path, 'rb') as file:
                header_data = file.read(struct.calcsize(self.header))
                head = struct.unpack(self.header, header_data)
                compressed_data = file.read(head[2])
                return compressed_data
        
        except Exception as e:
            self.logger.error(f"An error occurred while reading the VPK package:", e)
            raise VpkError("An error occurred while reading the VPK package.")
    
    def _read_dir(self, dir_path: str) -> dict:
        """
        Read a directory and return the data as a dictionary with the filenames as keys and the file data as values.
        
        Args:
            dir_path (str): The path to the directory.
            
        Returns:
            dict: A dictionary with the filenames as keys and the file data as values.
        """
        try:
            file_list = ValkyrieTools.getFileList(dir_path)
            byte_dict = {}
            for file in file_list:
                byte_dict[file] = ValkyrieTools.getFileData(file)
            return byte_dict
        
        except Exception as e:
            self.logger.error(f"An error occurred while reading the directory:", e)
            raise VpkError("An error occurred while reading the directory.")
    
    def _create_header(self, vpk_path: str, encrypted_data: bytes) -> bytes:
        """
        Create the VPK package header.
        
        Args:
            vpk_path (str): The path to the VPK file.
            encrypted_data (bytes): The encrypted data of the VPK package.
            
        Raises:
            VpkError: If an error occurred while creating the VPK package header.
            
        Returns:
            bytes: The header data of the VPK package.
        """
        try:
            filename = vpk_path.split("/")[-1].replace(".vpk", "").encode('utf-8')
            fileinfo = "Encrypted data package".encode('utf-8')
            filesize = len(encrypted_data)
            author = self.author.encode('utf-8')
            copyright = "Valky ⓒ 2023".encode('utf-8')
            timestamp = int(time.time())
            encryption = self.encryption.encode('utf-8')
            key_length = len(self.argon_key)
            version = self.version
            compression = self.compression.encode('utf-8')
    
            header_data = struct.pack(self.header, filename, fileinfo, filesize, author, copyright, timestamp, encryption, key_length, version, compression)
            return header_data
        
        except Exception as e:
            self.logger.error(f"An error occurred while creating the VPK package header:", e)
            raise VpkError("An error occurred while creating the VPK package header.")
        
    def _save(self, header_data: bytes, compressed_data: bytes, vpk_path: str) -> str:
        """
        Save the VPK package and return the path to the VPK package.
        
        Args:
            header_data (bytes): The header data of the VPK package.
            compressed_data (bytes): The compressed data of the VPK package.
            vpk_path (str): The path where the VPK package should be saved.
            
        Raises:
            VpkError: If an error occurred while writing the VPK package.
            
        Returns:
            str: The path to the VPK package.
        """
        try:
            vpk = header_data + compressed_data
            with open(vpk_path, 'wb') as file:
                file.write(vpk)
            return vpk_path
                
        except Exception as e:
            self.logger.error(f"An error occurred while writing the VPK package:", e)
            raise VpkError("An error occurred while writing the VPK package.")


if __name__ == "__main__":
    
    # ================================
    
    # V1: Generate a crypto key
    _key = '0123456789abcdef0123456789abcdef'
    _iv = '0123456789abcdef'
    crypto_key = ValkyrieCrypto.generate_argon_key(_key, _iv)
    # Initialize the class
    VPK = ValkyriePackage(crypto_key)
    
    # ================================
    print("-" * 50)
    # ================================
    
    # Read the example VPK package
    package_content = VPK.read(r"./examples/example.vpk")
    package_info = VPK.info(r"./examples/example.vpk")
    print(f"Package.v2: {package_info['filename']}")
    print(f"Package.v2: files: {len(package_content.keys())}")
    print(f"Package.v2: size: {ValkyrieTools.formatSize(package_info['filesize'])}")
    print(f"Package.v2: author: {package_info['author']}")
    print(f"Package.v2: copyright: {package_info['copyright']}")
    print(f"Package.v2: timestamp: {package_info['timestamp']}")
    print(f"Package.v2: encryption: {package_info['encryption']}")
    print(f"Package.v2: key length: {package_info['key_length']}")
    print(f"Package.v2: version: {package_info['version']}")
    print(f"Package.v2: compression: {package_info['compression']}")
    
    # ================================
    print("-" * 50)
    # ================================
    
    # V2: Create a new VPK package reading a directory
    package_path = VPK.create("./examples", "examples/out/example2.vpk")
    print("New VPK package successfully created!")
    
    # V2: Read the new VPK package
    package_content = VPK.read(package_path)
    package_info = VPK.info(package_path)
    print(f"Package.v2: {package_info['filename']}")
    print(f"Package.v2: files: {len(package_content.keys())}")
    print(f"Package.v2: size: {ValkyrieTools.formatSize(package_info['filesize'])}")
    print(f"Package.v2: author: {package_info['author']}")
    print(f"Package.v2: copyright: {package_info['copyright']}")
    print(f"Package.v2: timestamp: {package_info['timestamp']}")
    print(f"Package.v2: encryption: {package_info['encryption']}")
    print(f"Package.v2: key length: {package_info['key_length']}")
    print(f"Package.v2: version: {package_info['version']}")
    print(f"Package.v2: compression: {package_info['compression']}")
    
    # ================================
    print("-" * 50)
    # ================================
    