# Valkyrie Utils

Valkyrie Utils is a Python utility library that provides convenient and flexible functionalities through its four main modules: Logger, Config, Options, Compressor, Crypto and Tools.

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
  - [Tools](#valkyrie-tools)
- [Example Usage](#example-usage)

## About

This utility library was created to demonstrate how to use ValkyrieUtils modules in Python applications. The modules 
offer functionality to facilitate common tasks such as logging, configuration parsing, command-line option parsing, 
data compression, data encryption, and data validation.

## Usage

To use Valkyrie Utils, you'll need to import the desired module(s) into your Python script and follow the provided 
guidelines and examples. Here's a brief overview of each module:

- **Logger**: Facilitates easy logging with configurable log levels and file handling.
- **Config**: Enables easy reading and parsing of configuration files (INI, XML and JSON).
- **Options**: Allows you to define and parse command-line options with specified data types and default values.
- **Compressor**: Provides a utility to compress and decompress data using various compression modes.
- **Crypto**: Offers functions to encrypt and decrypt data using AES-GCM, AES-CTR, and AES-CBC.
- **Manifest**: Provides a class to create a Valkyrie Manifest, and to download missing or modified files from a remote URL.
- **Tools**: Provides various functions such as data validation, data type matching, code generation, and more.

## Modules

### Valkyrie Logger

The Logger module (`Logger.py`) provides a flexible logging solution for Python applications. It allows you to set the log level, define log file paths, and toggle debug mode.
> - Refer to the [Valkyrie Logger documentation](./readme/logger.md) for more information.

### Valkyrie Config

The Config module (`Config.py`) facilitates reading and parsing configuration files, supporting INI, XML and JSON formats. It provides methods to extract configuration values in various data types.
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

### Valkyrie Tools

The Tools module (`Tools.py`) offers functions to facilitate common tasks such as data validation, data type matching, code generation, and more, making it a useful utility module.
> - Refer to the [Valkyrie Tools documentation](./readme/tools.md) for more information.

## Example Usage

```python
# Example usage of ValkyrieUtils modules
# Run this script with the following command: python ValkyrieUtils.py --config_file examples/example.xml

from Logger import ValkyrieLogger
from Config import ValkyrieConfig
from Tools import ValkyrieTools
from Options import ValkyrieOptions
from Compressor import ValkyrieCompressor
from Crypto import ValkyrieCrypto, AES_GCM

# Create a new logger instance
logger = ValkyrieLogger('debug', 'logs/logger.log', 'ValkyrieUtils', True)
logger.info('Loading a new Valkyrie Logger instance')

# Initialize the command line options
parser = ValkyrieOptions([
  ('config_file', 'str', 'Configuration File Path and filename', 'examples/example.ini'),
])
options = parser.parse()
ext = options.config_file.split('.')[-1]

# Read the configuration file
config = ValkyrieConfig(f'examples/example.{ext}')

# Get the complete configuration as a dictionary
config_dict = ValkyrieTools.matchDict(config.get_config())

# Get the configuration nodes as a dictionary
config_dict_1 = ValkyrieTools.matchDict(config.get_dict("Test1"))
config_dict_2 = ValkyrieTools.matchDict(config.get_dict("Test2"))

# Compress the configuration data
compressed_config = ValkyrieCompressor.deflate(pickle.dumps(config_dict), 'zstd')

# Create a new argon encryption key
_key = ValkyrieTools.generateCode(64)
_iv = ValkyrieTools.generateCode(24)
argon_key = ValkyrieCrypto.generate_argon_key(_key, _iv)

# Encrypt the compressed configuration data
encrypted_config = ValkyrieCrypto.encrypt_data(argon_key, compressed_config, AES_GCM)

# Decrypt the ciphertext
decryption_config = ValkyrieCrypto.decrypt_data(argon_key, encrypted_config, AES_GCM)

# Decompress the configuration data
decompressed_config = pickle.loads(ValkyrieCompressor.inflate(decryption_config, 'zstd'))
```

The above example showcases how to utilize ValkyrieUtils modules in a Python script. Modify the `run_test` function as needed to suit your application's requirements.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

