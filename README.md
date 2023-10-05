# Valkyrie Utils

Valkyrie Utils is a Python utility library that provides various modules to facilitate common tasks such as logging, 
configuration parsing, command-line option parsing, data compression, data encryption, and data validation.

## Table of Contents

- [About](#about)
- [Usage](#usage)
- [Modules](#modules)
  - [Logger](#valkyrie-logger)
  - [Config](#valkyrie-config)
  - [Options](#valkyrie-options)
  - [Compressor](#valkyrie-compressor)
  - [Crypto](#valkyrie-crypto)
  - [Manifest](#valkyrie-manifest)
  - [Package](#valkyrie-package)
  - [Tools](#valkyrie-tools)
- [Examples](#examples)
- [Community](#community)
  - [Creator](#creator)
  - [Contribution](#contribution)
  - [Acknowledgements](#acknowledgements)
- [License](#license)

## About

Valkyrie Utils is a Python utility library that provides various modules to facilitate common tasks such as logging, 
configuration parsing, command-line option parsing, data compression, data encryption, and data validation.

The library is designed to simplify the development of Python applications by offering ready-to-use modules that 
handle essential functionalities, saving you time and effort in implementing these features from scratch.

Valkyrie Utils aims to be a versatile and user-friendly toolkit, suitable for a wide range of Python projects, 
from simple scripts to complex applications. Whether you need to manage configuration files, create secure and 
compressed data packages, or log application events, Valkyrie Utils has you covered.

The library is actively maintained and expanded to meet the evolving needs of Python developers. It is open-source 
and available for use in your projects under the MIT License.


## Usage

To use Valkyrie Utils, you'll need to import the desired module(s) into your Python script and follow the provided 
guidelines and examples. Here's a brief overview of each module:

- **Logger**: Facilitates easy logging with configurable log levels and file handling.
- **Config**: Enables easy reading and parsing of configuration files (INI, XML and JSON).
- **Options**: Allows you to define and parse command-line options with specified data types and default values.
- **Compressor**: Provides a utility to compress and decompress data using various compression modes.
- **Crypto**: Offers functions to encrypt and decrypt data using AES-GCM, AES-CTR, and AES-CBC.
- **Manifest**: Provides a class to create a Valkyrie Manifest, and to download missing or modified files from a remote URL.
- **Package**: Enables the creation, reading, and updating of encrypted VPK (Valkyrie Package) files.
- **Tools**: Provides various functions such as data validation, data type matching, code generation, and more.

---

## Modules

### Valkyrie Logger

The Logger module (`Logger.py`) provides a flexible logging solution for Python applications. It allows you to set the log level, define log file paths, and toggle debug mode.
> - Refer to the [Valkyrie Logger documentation](./readme/logger.md) for more information.

### Valkyrie Config

The Config module (`Config.py`) facilitates reading and parsing configuration files, supporting INI, XML, JSON and VCF formats. It provides methods to extract configuration values in various data types.
> - Refer to the [Valkyrie Config documentation](./readme/config.md) for more information.

### Valkyrie Options

The Options module (`Options.py`) helps manage command-line options by allowing easy definition of options with specified data types, help messages, and default values. The parsed options can be accessed through a dictionary-like interface.
> - Refer to the [Valkyrie Options documentation](./readme/options.md) for more information.

### Valkyrie Compressor
The Compressor module (`Compressor.py`) provides a utility to compress and decompress data using various compression modes, ranging from fast compression with low file size reduction to slow compression with high file size reduction.
> - Refer to the [Valkyrie Compressor documentation](./readme/compressor.md) for more information.

### Valkyrie Crypto
The Crypto module (`Crypto.py`) provides functions to encrypt and decrypt data using AES-GCM, AES-CTR, and AES-CBC with an Argon2 generated encryption key, which is derived from a user-provided key and initialization vector.
> - Refer to the [Valkyrie Crypto documentation](./readme/crypto.md) for more information.

### Valkyrie Manifest
The Manifest module (`Manifest.py`) provides a class to create a Valkyrie Manifest, a JSON file that contains files and their hashes. This manifest is crucial for verifying the integrity of a directory of files, and to download missing or modified files from a remote URL.
> - Refer to the [Valkyrie Manifest documentation](./readme/manifest.md) for more information.

### Valkyrie Package
The Package module (`Package.py`) enables the creation, reading, and updating of encrypted VPK (Valkyrie Package) files. VPK files are designed to store data in a compressed and encrypted format. This module provides functionality for handling encryption, decryption, compression, and file management within VPK files.
> - Refer to the [Valkyrie Package documentation](./readme/package.md) for more information.

### Valkyrie Tools

The Tools module (`Tools.py`) offers functions to facilitate common tasks such as data validation, data type matching, code generation, and more, making it a useful utility module.
> - Refer to the [Valkyrie Tools documentation](./readme/tools.md) for more information.

---

## Examples

You can find example usage of the Valkyrie Utils modules in the according readme files.

- [Valkyrie Logger](./readme/logger.md#example) (Logger.py)
- [Valkyrie Config](./readme/config.md#example) (Config.py)
- [Valkyrie Options](./readme/options.md#example) (Options.py)
- [Valkyrie Compressor](./readme/compressor.md#example) (Compressor.py)
- [Valkyrie Crypto](./readme/crypto.md#example) (Crypto.py)
- [Valkyrie Manifest](./readme/manifest.md#example) (Manifest.py)
- [Valkyrie Package](./readme/package.md#example) (Package.py)
- [Valkyrie Tools](./readme/tools.md#example) (Tools.py)

## Unittests

Each module in Valkyrie Utils has accompanying unittests located in the "unittests" folder. 
These unittests are essential for ensuring the correct functionality of the modules and maintaining code quality. 
To run the unittests for a specific module, use a Python testing framework like `unittest` or `pytest` and point it to the relevant test files in the "unittests" folder.

- `ValkyrieLogger` - `python -m unittest unittests/test_logger.py`
- `ValkyrieConfig` - `python -m unittest unittests/test_config.py`
- `ValkyrieOptions` - `python -m unittest unittests/test_options.py`
- `ValkyrieCompressor` - `python -m unittest unittests/test_compressor.py`
- `ValkyrieCrypto` - `python -m unittest unittests/test_crypto.py`
- `ValkyrieManifest` - `python -m unittest unittests/test_manifest.py`
- `ValkyriePackage` - `python -m unittest unittests/test_package.py`
- `ValkyrieTools` - `python -m unittest unittests/test_tools.py`

## Community

### Creator

This project was created by and is maintained by [Valky Fischer](https://valky.dev/en). Contact me if needed.
- [@v_lky](https://discord.gg/vky) on Discord
- [@v_lky](https://twitch.tv/v_lky) on Twitch
- [@ValkyDev](https://twitter.com/ValkyDev) on Twitter


### Contribution

Contributions to Valkyrie Utils are welcome and appreciated. 

By contributing to this project, you help make it better and more useful for everyone.  
Here are a few guidelines to follow: [Contribution Guidelines](CONTRIBUTION.md)


### Acknowledgements

I would like to acknowledge the following contributors for their support and contributions to this project:
- *None*

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

