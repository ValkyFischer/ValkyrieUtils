#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 03, 2023
@author: v_lky

--------

About:
    A class to create a valkyrie manifest, which is a json file that contains a list of files and their hashes. It
    can be used to verify the integrity of a directory of files, and to download missing or modified
    files from a remote url.

--------

Example:
    >>> dir_path = r"D:\path\to\examples\download\ARIA"
    >>> save_path = (r".\examples", "manifest")
    # Initialize the manifest creator
    >>> VM = ValkyrieManifest(app_path, save_path, debug=False)
    # Load local and remote manifests
    >>> local_manifest = VM.loadManifest("examples/manifest_full.json")
    >>> remote_manifest = VM.loadManifest("http://example.com/remote_url/manifest.json")
    # Check for modified files
    >>> files_to_update = VM.check(local_manifest, remote_manifest)
    # Download modified and missing files
    >>> VM.download(files_to_update, "http://example.com/remote_url")
    # Change the manifest name
    >>> VM.save_name = "manifest_full"
    # Change to include full data
    >>> VM.full = True
    # Create a clean manifest with full data
    >>> VM.createManifest()
    # Create a manifest with full data and update it with the files to update
    >>> VM.updateManifest(local_manifest, files_to_update)

"""

import json
import logging
import math
import os
import time
import concurrent.futures
import urllib.request

from tqdm import tqdm
from multiprocessing import cpu_count
from Tools import ValkyrieTools


class ValkyrieManifest:
    """
    A class to create a valkyrie manifest, which is a json file that contains a list of files and their hashes. It
    can be used to verify the integrity of a directory of files, and to download missing or modified
    files from a remote url.
    
    Args:
        directory (str | tuple[str, str]): The directory to create the manifest for. Can be a tuple of (directory, short_directory) to replace the directory with a shorter name in the manifest.
        save_as (tuple[str, str]): The directory and filename to save the manifest to. Can be a tuple of (directory, filename) to save the manifest to a different directory and filename.
        full (bool): Whether to include the full data in the manifest, including hash, filesize and modified date. Default is False.
        logger (logging.Logger): The logger to use. Default is False. If False, a logger will be created.
        debug (bool): Whether to enable debug logging. Default is False.
        
    Example:
        >>> dir_path = r"D:\path\to\examples\download\ARIA"
        >>> save_path = (r".\examples", "manifest")
        # Initialize the manifest creator
        >>> VM = ValkyrieManifest(app_path, save_path, debug=False)
        # Load local and remote manifests
        >>> local_manifest = VM.loadManifest("examples/manifest_full.json")
        >>> remote_manifest = VM.loadManifest("http://example.com/remote_url/manifest.json")
        # Check for modified files
        >>> files_to_update = VM.check(local_manifest, remote_manifest)
        # Download modified and missing files
        >>> VM.download(files_to_update, "http://example.com/remote_url")
        # Change the manifest name
        >>> VM.save_name = "manifest_full"
        # Change to include full data
        >>> VM.full = True
        # Create a clean manifest with full data
        >>> VM.createManifest()
        # Create a manifest with full data and update it with the files to update
        >>> VM.updateManifest(local_manifest, files_to_update)
        
        
        
    """
    def __init__(self, directory: str | tuple[str, str],  save_as: tuple[str, str] = False, full: bool = False, logger: logging.Logger = False, debug: bool = False):
        self.start = time.time()
        raw_dir = directory[0] if isinstance(directory, tuple) else directory
        self.dir = raw_dir.replace("\\", "/")
        raw_short_dir = directory[1] if isinstance(directory, tuple) else self.dir.split("/")[-1]
        self.short_dir = raw_short_dir.replace("\\", "/")
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

    def download(self, file_list, remote_url):
        """
        Downloads the given list of files from the given remote url.
        
        Args:
            file_list (list[str]): The list of files to download.
            remote_url (str): The remote url to download the files from.
            
        Raises:
            TypeError: If file_list is not a list.
            
        Returns:
            bool: True if the files were downloaded successfully, False otherwise, or None if there were no files to download.
        """
        self.logger.info("Downloading files...")
        
        if not isinstance(file_list, list):
            raise TypeError("file_list must be a list of file paths")
        
        if len(file_list) == 0:
            self.logger.info("No files to download")
            return None
        
        try:
            for file_path in tqdm(file_list, desc="Downloading", unit=" file"):
                self.downloadFile(file_path, remote_url)
            
            self.logger.info(f"Downloaded {len(file_list)} files")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to download files: {str(e)}")
            return False

    def check(self, local_manifest, remote_manifest):
        """
        Checks the given local and remote manifests for modified files.
        
        Args:
            local_manifest (dict): The local manifest to check.
            remote_manifest (dict): The remote manifest to check.
            
        Returns:
            list[str]: The list of files to update or download.
        """
        self.logger.info("Checking all files...")
        
        files_to_update = []
        files_to_update.extend(self.compareFiles(local_manifest))
        files_to_update.extend(self.compareManifest(local_manifest, remote_manifest))
        
        self.logger.info(f"Found {len(files_to_update)} files to update or download")
        return files_to_update
    
    def createManifest(self):
        """
        Creates a manifest of the files in the given directory.
        """
        self.logger.info("Starting manifest creation...")
        if self.debug: self.logger.debug(f"Gathering files: 0% | Time elapsed: {round(time.time() - self.start, 3)}s")
        file_list = ValkyrieTools.getFileList(self.dir)
        if self.debug: self.logger.debug(f"Gathering files: 100% | {len(file_list)} | Time elapsed: {round(time.time() - self.start, 3)}s")
        
        if len(file_list) <= 0:
            self.logger.info("No files found")
            return
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
        
    def updateManifest(self, local_manifest, update_paths):
        """
        Updates the given local manifest with the given update paths.
        
        Args:
            local_manifest (dict): The local manifest to update.
            update_paths (list[str]): The list of paths to update.
            
        Returns:
            dict: The updated manifest.
        """
        self.logger.info("Updating manifest...")
        if len(update_paths) > 0:
            if self.dir not in update_paths[0]:
                update_paths = [os.path.join(self.dir.replace(self.short_dir, ""), path) for path in update_paths]
                
            for file_path in tqdm(update_paths, desc = "Hashing", unit = " file"):
                local_manifest.update(self.getHash(file_path))
        
        else:
            self.logger.info("No files to update")
            
        return local_manifest
    
    def saveManifest(self, hashes: dict):
        """
        Saves the manifest to a file.
        
        Args:
            hashes (dict): The hashes to save.
        """
        with open(f'{self.save_path}/{self.save_name}.json', 'w') as file:
            file.write(json.dumps(hashes, indent = '\t'))

    def compareManifest(self, local_manifest, remote_manifest):
        """
        Compares the given local and remote manifests for missing files.
        
        Args:
            local_manifest (dict): The local manifest to check.
            remote_manifest (dict): The remote manifest to check.
            
        Returns:
            list[str]: The list of files to download.
        """
        
        missing_files = []
        for file_path in remote_manifest:
            if file_path not in local_manifest:
                if file_path not in missing_files:
                    missing_files.append(file_path.replace("\\", "/"))
            elif not os.path.exists(os.path.join(self.dir.replace(self.short_dir, ""), file_path)):
                if file_path not in missing_files:
                    missing_files.append(file_path.replace("\\", "/"))
        
        if self.debug: self.logger.debug(f"Missing files: {len(missing_files)}")
        return missing_files

    def loadManifest(self, manifest_path):
        """
        Loads the manifest from the given path. Can be a local path or a remote url.
        
        Args:
            manifest_path (str): The path to the manifest.
        
        Raises:
            TypeError: If manifest_path is not a json file.
            FileNotFoundError: If the manifest file is not found.
            
        Returns:
            dict: The loaded manifest.
        """
        if manifest_path.startswith("http"):
            if self.debug: self.logger.debug(f"Loading remote manifest: {manifest_path}")
            with urllib.request.urlopen(manifest_path) as url:
                url_data = url.read().decode()
                if not ValkyrieTools.isJson(url_data):
                    raise TypeError(f"Manifest path must be a json file: {url_data}")
                return json.loads(url_data)
            
        elif os.path.exists(manifest_path):
            if self.debug: self.logger.debug(f"Loading local manifest: {manifest_path}")
            with open(manifest_path, "r") as f:
                json_data = f.read()
                if not ValkyrieTools.isJson(json_data):
                    raise TypeError(f"Manifest path must be a json file: {manifest_path}")
                return json.loads(json_data)
            
        else:
            raise FileNotFoundError(f"Manifest file not found: {manifest_path}")
    
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
    
    def getHash(self, file_paths: str | list[str]):
        """
        Gets the hash of the given file paths.
        
        Args:
            file_paths (str | list[str]): The list of file paths to get the hash of. Can be a single file path.
            
        Returns:
            dict: The hashes of the files.
        """
        hashes = {}
        if isinstance(file_paths, str):
            file_paths = [file_paths]
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
    
    def compareFiles(self, local_manifest):
        """
        Compares the given local manifest for modified files.
        
        Args:
            local_manifest (dict): The local manifest to check.
            
        Returns:
            list[str]: The list of files to update.
        """
        modified_files = []
        for file_path, local_file_info in local_manifest.items():
            if not self.checkFile(file_path, local_file_info):
                modified_files.append(file_path)
        
        if self.debug: self.logger.debug(f"Modified files: {len(modified_files)}")
        return modified_files

    def downloadFile(self, file_path, remote_url):
        """
        Downloads the given file from the given remote url.
        
        Args:
            file_path (str): The file to download.
            remote_url (str): The remote base url to download the file from.
            
        Raises:
            TypeError: If file_path is not a string.
            
        Returns:
            bool: True if the file was downloaded successfully, False otherwise.
        """
        remote_file_path = remote_url + "/" + file_path.replace("./", "")
        local_file_path = os.path.join(self.dir.replace(self.short_dir, ""), file_path)
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        try:
            urllib.request.urlretrieve(remote_file_path, local_file_path)
            return True
        except Exception as e:
            self.logger.error(f"Failed to download {file_path}: {str(e)}")
            return False

    def checkFile(self, file_path, local_file_info):
        """
        Checks the given file path against the given local file info.
        
        Args:
            file_path (str): The file path to check.
            local_file_info (str | list[str, int, str]): The local file info to check.
            
        Returns:
            bool: True if the file is up-to-date, False otherwise.
        """
        absolute_path = os.path.join(self.dir, file_path)
        if os.path.exists(absolute_path):
            local_hash = ValkyrieTools.getFileHash(absolute_path)
            if isinstance(local_file_info, list) or isinstance(local_file_info, tuple):
                if local_hash != local_file_info[0]:
                    return False
            elif isinstance(local_file_info, str):
                if local_hash != local_file_info:
                    return False
        
        return True


if __name__ == "__main__":
    # Set the app paths
    app_dir = r".\examples\download\ARIA"
    app_replace = r"ARIA"
    app_path = (app_dir, app_replace)
    
    # Set the save paths
    save_dir = r".\examples"
    save_name = "manifest"
    save_path = (save_dir, save_name)

    # Prepare manifests
    _remote_url = "http://download.valkyteq.com/v-utils"
    _local_manifest_path = "examples/manifest_full.json"
    _remote_manifest_path = _remote_url + "/manifest.json"
    
    # Initialize the manifest creator
    VM = ValkyrieManifest(app_dir, save_path, debug=False)
    
    # Load local and remote manifests
    _local_manifest = VM.loadManifest(_local_manifest_path) if os.path.exists(_local_manifest_path) else {}
    _remote_manifest = VM.loadManifest(_remote_url + "/manifest.json")

    # Check for modified files
    _files_to_update = VM.check(_local_manifest, _remote_manifest)
    
    # Download modified and missing files
    VM.download(_files_to_update, _remote_url)
    
    # Change the manifest name
    VM.save_name = "manifest_full"
    # Change to include full data
    VM.full = True
    # Create the manifest with full data
    _new_manifest = VM.updateManifest(_local_manifest, _files_to_update)
    
    # Save the manifest
    VM.saveManifest(_new_manifest)
