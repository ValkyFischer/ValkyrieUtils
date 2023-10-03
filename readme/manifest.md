## Valkyrie Manifest Module

The Manifest module (`Manifest.py`) provides a class to create a Valkyrie Manifest, a JSON file that contains 
files and their hashes. This manifest is crucial for verifying the integrity of a directory of files, and to download 
missing or modified files from a remote URL.

### Usage: Download Manifest Files

Here is an example of how to use the Manifest module to download missing or modified files from a remote URL:
1. Import the Manifest module into your Python script.
2. Create an instance of the `ValkyrieManifest` class, specifying the directory to create the manifest for and the save location.
3. Load local and remote manifests using the `loadManifest()` method.
4. Check for modified files using the `check()` method.
5. Download modified and missing files using the `download()` method.
6. Update the local manifest with the files to update using the `updateManifest()` method.
   - Optionally, you can specify the `full` parameter to include file size and last modified date in the manifest.
7. Save the manifest using the `saveManifest()` method.

### Usage: Creating Manifest Only

Here is an example of how to use the Manifest module to create a manifest without downloading any files:
1. Import the Manifest module into your Python script.
2. Create an instance of the `ValkyrieManifest` class, specifying the directory to create the manifest for and the save location.
3. Create a clean manifest using the `createManifest()` method.
   - Optionally, you can specify the `full` parameter to include file size and last modified date in the manifest.


### Example

```python
from Manifest import ValkyrieManifest

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
```

### Supported Classes and Functions

- `ValkyrieManifest`: A class to create a manifest of files in a directory.
    - `createManifest()`: Creates the manifest.
    - `saveManifest(hashes: dict)`: Saves the manifest to a file.
    - `hashingFiles(file_list)`: Hashes the files in the given file list.
    - `getHash(file_paths: str | list[str])`: Gets the hash of the given file paths.
    - `compareFiles(local_manifest)`: Compares the given local manifest for modified files.
    - `compareManifest(local_manifest, remote_manifest)`: Compares the given local and remote manifests for missing files.
    - `downloadFile(file_path, remote_url)`: Downloads the given file from the given remote URL.
    - `checkFile(file_path, local_file_info)`: Checks the given file path against the given local file info.
    - `download(file_list, remote_url)`: Downloads the given list of files from the given remote URL.
    - `check(local_manifest, remote_manifest)`: Checks the given local and remote manifests for modified files.
    - `updateManifest(local_manifest, update_paths)`: Updates the given local manifest with the given update paths.
    - `loadManifest(manifest_path)`: Loads the manifest from the given path. Can be a local path or a remote URL.

### Manifest Structure

- Basic Manifest:
    The manifest is a JSON file that contains a list of files and their hashes. The structure of the manifest is as follows:
    
    ```json
    {
        "file1.txt": "md5hash1",
        "file2.txt": "md5hash2"
    }
    ```

- Full Manifest:
    The full manifest is a JSON file that contains files and their hashes, as well as their file size and last modified date. The structure of the manifest is as follows:
    
    ```json
    {
        "file1.txt": [
            "md5hash1", 123, "2021-01-01 00:00:00"
        ],
        "file2.txt": [
            "md5hash2", 456, "2021-01-01 00:00:00"
        ]
    }
    ```

---

### Notes

- *Requires the `ValkyrieTools` module.*
