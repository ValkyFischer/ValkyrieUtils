## Valkyrie Package Module

The Valkyrie Package module (`ValkyriePackage.py`) is a Python module that enables the creation, reading, and updating of VPK (Valkyrie Package) files. VPK files are designed to store data in a compressed and encrypted format. This module provides functionality for handling encryption, decryption, compression, and file management within VPK files.

### Usage

1. Import the Valkyrie Package module into your Python script.
2. Initialize the `ValkyriePackage` class by providing an Argon2 key.
3. Utilize the provided methods to create, read, update, and manage VPK packages.

### Example

```python
from Package import ValkyriePackage

# Initialize ValkyriePackage with an Argon2 key
crypto_key = b"YourArgonCryptoKey"
VPK = ValkyriePackage(crypto_key)

# Get information about a VPK package
vpk_info = VPK.info("examples/example.vpk")

# Read an existing VPK package
vpk_content = VPK.read("examples/example.vpk")

# Save a VPK package from a dictionary
VPK.save(vpk_content, "examples/out/example.vpk")

# Create a new VPK package from a directory
VPK.create("/path/to/directory", "path/to/save/package.vpk")

# Update an existing VPK package
VPK.update(vpk_content, "path/to/existing/package.vpk")
```

In this example, we demonstrate how to create, read, and update VPK packages using the Valkyrie Package module.

## Supported Classes and Functions

- `ValkyriePackage`: The main class for handling VPK packages.
  - `info(vpk_path: str) -> dict`: Get information about a VPK file.
  - `read(vpk_path: str) -> dict`: Read a VPK package and return decrypted data.
  - `create(dir_path: str, vpk_path: str = None) -> str`: Create a VPK package from a directory.
  - `save(byte_dict: dict, vpk_path: str) -> str`: Save a VPK package from a dictionary.
  - `update(byte_dict: dict, vpk_path: str) -> str`: Update an existing VPK package.

## VPK File Structure

VPK files are structured as follows:

```
VPK Package 
│
├── Header
│   ├── VPK Name
│   ├── VPK Info
│   ├── Data Size
│   ├── Author
│   ├── Copyright
│   ├── Timestamp
│   ├── Encryption
│   ├── Key Size
│   ├── Version
│   ├── Compression
│
├── Encrypted Data
│   ├── Files 1
│   │   ├── File Path
│   │   ├── File Data
│   │
│   ├── Files 2
│   │   ├── File Path
│   │   ├── File Data
│   │
│   ├── ...
```

#### VPK Header

The VPK header is a JSON object that contains information about the VPK package.

| Key | Description |
| --- | --- |
| `VPK Name` | The name of the VPK package. |
| `VPK Info` | A description of the VPK package. |
| `Data Size` | The size of the VPK package in bytes. |
| `Author` | The author of the VPK package. |
| `Copyright` | The license of the VPK package. |
| `Timestamp` | The timestamp of the VPK package. |
| `Encryption` | The encryption algorithm used to encrypt the VPK package. |
| `Key Size` | The size of the encryption key in bytes. |
| `Version` | The version of the VPK package. |
| `Compression` | The compression algorithm used to compress the VPK package. |

#### VPK Encrypted Data

The VPK encrypted data is a dictionary that contains the file paths and data of the VPK package.

| Key | Description |
| --- | --- |
| `File Path` | The path of the file within the VPK package. |
| `File Data` | The data of the file within the VPK package. |

---

### Notes

To use the Valkyrie Package module, you will need the following modules from ValkyrieUtils:
- `ValkyrieCrypto`: For en/decryption. Supports AES-GCM, AES-CTR, and AES-CBC.
- `ValkyrieCompressor`: For compression. Supports Gzip, ZSTD, Bzip2, LZMA, and LZ4.
