#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 03, 2023
@author: v_lky

--------

About:
    A valkyrie manifest is a json file that contains a list of files and their hashes. It can be used to verify
    the integrity of a directory of files. This module provides a class to create a manifest.
--------

Example:
    >>> VM = ValkyrieManifest((r"C:\Temp", "Test"), (r".\examples\out", "manifest"))
    >>> VM.createManifest()

"""

import json
import logging
import math
import time
import concurrent.futures

from multiprocessing import cpu_count
from Tools import ValkyrieTools


class ValkyrieManifest:
    """
    A class to create a manifest of files in a directory.
    
    Args:
        directory (str | tuple[str, str]): The directory to create the manifest for. Can be a tuple of (directory, short_directory) to replace the directory with a shorter name in the manifest.
        save_as (tuple[str, str]): The directory and filename to save the manifest to. Can be a tuple of (directory, filename) to save the manifest to a different directory and filename.
        full (bool): Whether to include the full data in the manifest, including hash, filesize and modified date. Default is False.
        logger (logging.Logger): The logger to use. Default is False. If False, a logger will be created.
        debug (bool): Whether to enable debug logging. Default is False.
        
    Example:
        >>> VM = ValkyrieManifest((r"C:\Temp", "Test"), (r".\examples\out", "manifest"))
        >>> VM.createManifest()
        
    """
    def __init__(self, directory: str | tuple[str, str], save_as: tuple[str, str] = False, full: bool = False, logger: logging.Logger = False, debug: bool = False):
        self.start = time.time()
        raw_dir = directory[0] if isinstance(directory, tuple) else directory
        self.dir = raw_dir.replace("\\", "/")
        raw_short_dir = directory[1] if isinstance(directory, tuple) else False
        self.short_dir = raw_short_dir.replace("\\", "/") if raw_short_dir else False
        raw_save_path = save_as[0] if isinstance(save_as, tuple) else self.dir
        self.save_path = raw_save_path.replace("\\", "/")
        self.save_name = save_as[1] if isinstance(save_as, tuple) else "manifest"
        self.full = full
        self.debug = debug
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger("ValkyrieManifest")
            self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
            self.logger.addHandler(logging.StreamHandler())
    
    def createManifest(self):
        """
        Creates the manifest.
        """
        self.logger.info("Starting manifest creation...")
        if self.debug: self.logger.debug(f"Gathering files: 0% | Time elapsed: {round(time.time() - self.start, 3)}s")
        file_list = ValkyrieTools.getFileList(self.dir)
        if self.debug: self.logger.debug(f"Gathering files: 100% | {len(file_list)} | Time elapsed: {round(time.time() - self.start, 3)}s")
        
        hash_dict = self.hashingFiles(file_list)
        
        if self.debug: self.logger.debug(f'Saving manifest: 0% | Time elapsed: {round(time.time() - self.start, 3)}s')
        self.saveManifest(hash_dict)
        if self.debug: self.logger.debug(f'Saving manifest: 100% | Time elapsed: {round(time.time() - self.start, 3)}s')
        
        self.logger.info("-" * 50)
        self.logger.info(f"Manifest path: {self.save_path}/{self.save_name}.json")
        self.logger.info(f"Total files hashed: {len(file_list)}")
        if not self.full:
            self.logger.info(f"Basic job finished: {round(time.time() - self.start, 3)}sec ({app_path[1]})")
        else:
            total_size = sum(item[1] for item in hash_dict.values())
            self.logger.info(f"Total files size: {ValkyrieTools.formatSize(total_size)}")
            self.logger.info(f"Full job finished: {round(time.time() - self.start, 3)}sec ({app_path[1]})")
        self.logger.info("-" * 50)
    
    def saveManifest(self, hashes: dict):
        """
        Saves the manifest to a file.
        
        Args:
            hashes (dict): The hashes to save.
        """
        with open(f'{self.save_path}/{self.save_name}.json', 'w') as file:
            file.write(json.dumps(hashes, indent = '\t'))
    
    def hashingFiles(self, file_list):
        """
        Hashes the files in the given file list.
        
        Args:
            file_list (list[str]): The list of files to hash.
            
        Returns:
            dict: The hashes of the files.
        """
        ifile = len(file_list)
        hash_dict = {}
        
        cps = []
        num_workers = cpu_count() if cpu_count() >= 8 else 8
        for i in range(num_workers + 1):
            cps.append(False)
        
        ix = 0
        chunk_size = int(math.ceil(ifile / num_workers))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers = num_workers) as executor:
            future_to_index = {
                executor.submit(self.getHash, file_list[i:i + chunk_size]): i for i in range(0, ifile, chunk_size)
            }
            if self.debug: self.logger.debug(f'Hashing files: 0% | Time elapsed: {round(time.time() - self.start, 3)}s')
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    hashes = future.result()
                    hash_dict.update(hashes)
                except Exception as exc:
                    if self.debug: self.logger.debug(f'Error hashing files: {exc}')
                finally:
                    ix += 1
                    frac = float(ix) / float(num_workers)
                    cpi = int(math.floor(frac * num_workers))
                    if not cps[cpi]:
                        cps[cpi] = True
                        perc = int(cpi * (100 / num_workers))
                        if self.debug: self.logger.debug(f'Hashing files: {perc}% | {int((ifile / 100) * perc)} | Time elapsed: {round(time.time() - self.start, 3)}s')
        
        return hash_dict
    
    def getHash(self, file_paths: list[str]):
        """
        Gets the hash of the given file paths.
        
        Args:
            file_paths (list[str]): The list of file paths to get the hash of.
            
        Returns:
            dict: The hashes of the files.
        """
        hashes = {}
        for file_path in file_paths:
            if self.short_dir:
                key_name = file_path.replace(self.dir, self.short_dir)
            else:
                key_name = file_path
            
            if self.full:
                hashes[key_name] = [ValkyrieTools.getFileHash(file_path, "md5"), ValkyrieTools.getFileSize(file_path), ValkyrieTools.getFileDate(file_path)]
            else:
                hashes[key_name] = ValkyrieTools.getFileHash(file_path, "md5")
        return hashes


if __name__ == "__main__":
    # Set the app paths
    app_dir = r"C:\Temp"
    app_replace = r"Test"
    app_path = (app_dir, app_replace)
    
    # Set the save paths
    save_dir = r".\examples\out"
    save_name = "manifest"
    save_path = (save_dir, save_name)
    
    # Initialize the manifest creator
    MC = ValkyrieManifest(app_path, save_path)
    # Create the manifest
    MC.createManifest()
    
    # Change the manifest name
    MC.save_name = "manifest_full"
    # Change to include full data
    MC.full = True
    # Create the manifest with full data
    MC.createManifest()
