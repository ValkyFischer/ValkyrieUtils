#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 01, 2023
@author: v_lky

--------

About:
    This module, ValkyrieCrypto, provides functions to encrypt and decrypt data using AES-GCM, AES-CTR, and AES-CBC.
    It also provides a function to generate a key using Argon2, a memory-hard function that is designed to be resistant
    to GPU cracking attacks. The argon-key will then be used to encrypt and decrypt data.

--------

Example:
    >>> key = '0123456789abcdef0123456789abcdef'
    >>> iv = '0123456789abcdef'
    >>> data = b'Hello, World!'
    
    >>> argon_key = ValkyrieCrypto.generate_argon_key(sample_key, sample_iv)
    b'\xe22\x04\xdd\xa9]U\x1a\xc6\x8b\x95\xa1\xb7\xacAqN\xef]\x9eP\t\xdc\xe6Hx\xc3\xa7\xcc(YO'
    
    >>> encrypted_data = ValkyrieCrypto.encrypt_data(argon_key, bytes_data)
    {'ciphertext': 'f2a2c4b2c4b2c4b2c4b2c4b2c4b2c4b2', 'tag': 'a2c4b2c4b2c4b2c4b2c4b2c4b2c4b2c4', 'iv': '0123456789abcdef'}
    
    >>> decrypted_data = ValkyrieCrypto.decrypt_data(argon_key, encrypted_data)
    Hello, World!

"""

import argon2
from Cryptodome.Cipher import AES
from Tools import ValkyrieTools


# ===============================


AES_GCM = 0
AES_CTR = 1
AES_CBC = 2
MODES_L = [AES_GCM, AES_CTR, AES_CBC]
MODES_D = {'AES-GCM': AES_GCM, 'AES-CTR': AES_CTR, 'AES-CBC': AES_CBC}


# ===============================


class ValkyrieCrypto:
    """
    A class to encrypt and decrypt data using AES-GCM, AES-CTR, and AES-CBC.
    
    Args:
        None
        
    Example:
        >>> key = '0123456789abcdef0123456789abcdef'
        >>> iv = '0123456789abcdef'
        >>> data = b'Hello, World!'
        
        >>> argon_key = ValkyrieCrypto.generate_argon_key(sample_key, sample_iv)
        >>> encrypted_data = ValkyrieCrypto.encrypt_data(argon_key, bytes_data)
        >>> decrypted_data = ValkyrieCrypto.decrypt_data(argon_key, encrypted_data)
    """
    
    @staticmethod
    def __key__() -> bytes:
        """
        Generate a unique key for encrypting and decrypting the configuration file.
        
        Returns:
            bytes: The generated key.
        """
        hwid = str(ValkyrieTools.generateHwid())
        key = ValkyrieCrypto.generate_argon_key(hwid * 2, hwid)
        return key
    
    @staticmethod
    def encrypt_data(key: bytes, data: any, mode: int = AES_CTR) -> dict:
        """Encrypts data using AES-GCM
    
        ---------------
    
        The encrypt_data function takes two arguments: 'key' and 'data'. The key argument is the encryption key used
        to encrypt the data argument.
    
        The function creates a new instance of the AES cipher in Galois/Counter Mode (GCM) using the key argument.
        It then encrypts the data argument using the cipher's encrypt_and_digest method. The resulting ciphertext
        is stored in ct_bytes, and the authentication tag is stored in tag.
    
        The function generates a nonce (number used once) using the cipher's nonce method and stores it in iv.
        The nonce is a random value that is used only once during encryption to ensure that the same plaintext
        encrypted multiple times does not result in the same ciphertext.
    
        The function then returns a dictionary containing the ciphertext, authentication tag, and nonce in hexadecimal
        format. These values are represented as strings using the hex() method, so they can be easily serialized and
        transmitted over a network.
    
        :param key: a byte string of length 16, 24, or 32 bytes
        :param data: any kind of data to encrypt
        :param mode: 0 for AES-GCM, 1 for AES-CTR, 2 for AES-CBC
        :return dict: dictionary containing the ciphertext, authentication tag, and nonce in hexadecimal format
        """
        if mode == AES_GCM:
            cipher = AES.new(key, AES.MODE_GCM)
            ct_bytes, tag = cipher.encrypt_and_digest(data)
            iv = cipher.nonce
            return {
                "ciphertext": ct_bytes.hex(),
                "tag": tag.hex(),
                "iv": iv.hex()
            }
        elif mode == AES_CTR:
            cipher = AES.new(key, AES.MODE_CTR)
            ct_bytes = cipher.encrypt(data)
            iv = cipher.nonce
            return {
                "ciphertext": ct_bytes.hex(),
                "iv": iv.hex()
            }
        elif mode == AES_CBC:
            cipher = AES.new(key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(data)
            iv = cipher.iv
            return {
                "ciphertext": ct_bytes.hex(),
                "iv": iv.hex()
            }
        else:
            raise ValueError("Invalid mode: 0 for AES-GCM, 1 for AES-CTR, 2 for AES-CBC")
    
    @staticmethod
    def decrypt_data(key: bytes, data: dict, mode: int = AES_CTR) -> str | bytes:
        """Decrypts data using AES-GCM
    
        ---------------
    
        The decrypt_data function takes two arguments: 'key' and 'data'. The key argument is the decryption
        key used to decrypt the data argument.
    
        The function first extracts the ciphertext, authentication tag, and nonce from the data argument,
        which is expected to be a dictionary containing these values in hexadecimal format.
    
        Next, the function creates a new instance of the AES cipher in GCM mode using the key argument and the
        nonce extracted from the data argument.
    
        The function then calls the cipher's decrypt_and_verify method, passing the ciphertext and authentication
        tag as arguments. If the authentication tag is invalid, indicating that the ciphertext has been tampered
        with, the method will raise a ValueError exception.
    
        If the authentication tag is valid, the method will return the decrypted plaintext, which is then decoded
        from bytes to a string using the decode method with the utf-8 encoding.
    
        The function returns the decrypted plaintext as a string.
    
        :param key: a byte string of length 16, 24, or 32 bytes used to decrypt the data
        :param data: dictionary containing the ciphertext, authentication tag, and nonce in hexadecimal format
        :param mode: 0 for AES-GCM, 1 for AES-CTR, 2 for AES-CBC
        :return str | bytes: decrypted plaintext as a string
        """
        if mode == AES_GCM:
            iv = bytes.fromhex(data['iv'])
            ct = bytes.fromhex(data['ciphertext'])
            tag = bytes.fromhex(data['tag'])
            cipher = AES.new(key, AES.MODE_GCM, nonce = iv)
            pt_bytes = cipher.decrypt_and_verify(ct, tag)
            try:
                return pt_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return pt_bytes
        elif mode == AES_CTR:
            iv = bytes.fromhex(data['iv'])
            ct = bytes.fromhex(data['ciphertext'])
            cipher = AES.new(key, AES.MODE_CTR, nonce = iv)
            pt_bytes = cipher.decrypt(ct)
            try:
                return pt_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return pt_bytes
        elif mode == AES_CBC:
            iv = bytes.fromhex(data['iv'])
            ct = bytes.fromhex(data['ciphertext'])
            cipher = AES.new(key, AES.MODE_CBC, iv = iv)
            pt_bytes = cipher.decrypt(ct)
            try:
                return pt_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return pt_bytes
        else:
            raise ValueError("Invalid mode: 0 for AES-GCM, 1 for AES-CTR, 2 for AES-CBC")
    
    @staticmethod
    def generate_argon_key(secret: str, salt: str, key_length: int = 32, time_cost: int = 2, memory_cost: int = 100, parallelism: int = 8) -> bytes:
        """
        Generates a key using Argon2
    
        -----------------
    
        The generate_argon_key function uses the Argon2 key derivation function to generate a key.
    
        Argon2 is a memory-hard function that is designed to be resistant to GPU cracking attacks, what can be used
        to derive cryptographic keys.
    
        The function first sets up the parameters for the Argon2 function:
    
        - secret: The secret value to use as input to the key derivation function.
        - salt: A random value used to add additional randomness to the key.
        - key_length: The length of the derived key, in bytes.
        - time_cost: The amount of time to spend on each iteration of the key derivation function. Increasing this value makes it more difficult to brute-force the derived key.
        - memory_cost: The amount of memory to use during the key derivation function. Increasing this value also makes it more difficult to brute-force the derived key.
        - parallelism: The number of parallel threads to use during the key derivation function.
    
        The function calls the argon2.low_level.hash_secret_raw method to generate the key using the provided
        parameters.
    
        This method returns a byte string containing the derived key.
    
        :param secret: The secret value to use as input to the key derivation function.
        :param salt: A random value used to add additional randomness to the key.
        :param key_length: The length of the derived key, in bytes.
        :param time_cost: The amount of time to spend on each iteration of the key derivation function.
        :param memory_cost: The amount of memory to use during the key derivation function.
        :param parallelism: The number of parallel threads to use during the key derivation function.
        :return bytes:
        """
        
        key = argon2.low_level.hash_secret_raw(
            secret = secret.encode('utf-8'),
            salt = salt.encode('utf-8'),
            time_cost = time_cost,
            memory_cost = memory_cost * 100,
            parallelism = parallelism,
            hash_len = key_length,
            type = argon2.low_level.Type.ID
        )
        
        return key


# ===============================


if __name__ == '__main__':
    # ================================
    print("-" * 50)
    # ================================
    
    # Test the encrypt_data and decrypt_data functions
    sample_key = '0123456789abcdef0123456789abcdef'
    sample_iv = '0123456789abcdef'
    bytes_data = b'Hello, World!'
    print('Byte-like data:', bytes_data)
    
    # Generate a key using Argon2
    encryption_key = ValkyrieCrypto.generate_argon_key(sample_key, sample_iv)
    print('Encryption key:', encryption_key)
    
    # Encrypt the plaintext
    encryption_data = ValkyrieCrypto.encrypt_data(encryption_key, bytes_data)
    print('Encrypted data:', encryption_data)
    
    # Decrypt the ciphertext
    decryption_data = ValkyrieCrypto.decrypt_data(encryption_key, encryption_data)
    print('Decrypted data:', decryption_data)

    # ================================
    print("-" * 50)
    # ================================
