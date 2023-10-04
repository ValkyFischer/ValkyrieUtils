#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 01, 2023
@author: v_lky

--------

About:
    This script provides a utility to compress and decompress data using various compression modes such as gzip,
    bzip2, lzma, lz4, zstd, and none (no compression). It offers functions to compress and decompress data based
    on the specified compression mode.

--------

Example:
    >>> data_to_compress = b"Sample data to be compressed"
    >>> compressed_data = ValkyrieCompressor.deflate(data_to_compress, 'zstd')
    >>> decompressed_data = ValkyrieCompressor.inflate(compressed_data, 'zstd')

"""

import gzip
import bz2
import lzma
import lz4.frame
import zstandard as zstd


# ===============================


class ValkyrieCompressor:
    """
    A class to compress and decompress data using various compression modes such as gzip, bzip2, lzma, lz4, zstd, and none (no compression).
    
    Args:
        None
        
    Example:
        >>> data = b"Sample data to be compressed"
        >>> compressed = ValkyrieCompressor.deflate(data, 'zstd')
        >>> decompressed = ValkyrieCompressor.inflate(compressed, 'zstd')
    """
    
    @staticmethod
    def deflate(raw_data, compression_mode = 'zstd'):
        """
        Compresses the given data using the specified compression mode.

        Args:
            raw_data: The data to be compressed.
            compression_mode: The compression mode to be used. Possible values are 'gzip', 'bzip2', 'lzma', 'lz4', 'zstd', and 'none'. Default is 'zstd'.

        Returns:
            The compressed data.
        """
        if not isinstance(raw_data, bytes):
            raise TypeError("Data to be compressed must be of type 'bytes'.")
        if compression_mode == 'gzip':
            return gzip.compress(raw_data)
        elif compression_mode == 'bzip2':
            return bz2.compress(raw_data)
        elif compression_mode == 'lzma':
            return lzma.compress(raw_data)
        elif compression_mode == 'lz4':
            return lz4.frame.compress(raw_data)
        elif compression_mode == 'zstd':
            return zstd.compress(raw_data)
        elif compression_mode == 'none' or compression_mode is None:
            return raw_data
        else:
            raise ValueError("Invalid compression mode. Supported modes are 'gzip', 'bzip2', 'lzma', 'lz4', 'zstd', and 'none' or None.")
    
    @staticmethod
    def inflate(compressed_data, compression_mode = 'zstd'):
        """
        Decompresses the given compressed data using the specified compression mode.

        Args:
            compressed_data: The compressed data to be decompressed.
            compression_mode: The compression mode that was used for compression. Possible values are 'gzip', 'bzip2', 'lzma', 'lz4', 'zstd', and 'none'. Default is 'zstd'.

        Returns:
            The decompressed data.
        """
        if not isinstance(compressed_data, bytes):
            raise TypeError("Data to be decompressed must be of type 'bytes'.")
        if compression_mode == 'gzip':
            return gzip.decompress(compressed_data)
        elif compression_mode == 'bzip2':
            return bz2.decompress(compressed_data)
        elif compression_mode == 'lzma':
            return lzma.decompress(compressed_data)
        elif compression_mode == 'lz4':
            return lz4.frame.decompress(compressed_data)
        elif compression_mode == 'zstd':
            return zstd.decompress(compressed_data)
        elif compression_mode == 'none' or compression_mode is None:
            return compressed_data
        else:
            raise ValueError("Invalid compression mode. Supported modes are 'gzip', 'bzip2', 'lzma', 'lz4', 'zstd', and 'none' / None.")


# ===============================


if __name__ == '__main__':

    # ================================
    print("-" * 50)
    # ================================
    
    # Run a test: zstd
    sample_data = b"Sample data to be compressed"
    sample_compressed = ValkyrieCompressor.deflate(sample_data, 'zstd')
    sample_decompressed = ValkyrieCompressor.inflate(sample_compressed, 'zstd')
    
    # Print the results
    print(f"Original data     : {sample_data}")
    print(f"Compressed data   : {sample_compressed}")
    print(f"Decompressed data : {sample_decompressed}")

    # ================================
    print("-" * 50)
    # ================================
