## Valkyrie Manifest Module

The Manifest module (`Manifest.py`) provides a class to create a Valkyrie Manifest, a JSON file that contains 
files and their hashes. This manifest is crucial for verifying the integrity of a directory of files. The manifest can
be created with or without the full data of the files, which includes the file size and last modified date.

### Usage

1. Import the Manifest module into your Python script.
2. Create an instance of the `ValkyrieManifest` class, specifying the directory to create the manifest for and the save location.
3. Call the `createManifest()` method to generate the manifest.
4. The manifest will be saved in the specified location as a JSON file, containing file names and their respective hashes.

***Note:*** *Requires the `ValkyrieTools` module to be in the same directory.*

### Example

```python
from Manifest import ValkyrieManifest

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
```

In this example, we create a basic manifest for the directory in `C:\Temp` and save it to the `examples/out` directory. We then
create a manifest with full data and save it to the same directory.

### Supported Classes and Functions

- `ValkyrieManifest`: A class to create a manifest of files in a directory.
    - `createManifest()`: Creates the manifest.
    - `saveManifest(hashes: dict)`: Saves the manifest to a file.
    - `hashingFiles(file_list)`: Hashes the files in the given file list.
    - `getHash(file_paths: list[str])`: Gets the hash of the given file paths.

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
