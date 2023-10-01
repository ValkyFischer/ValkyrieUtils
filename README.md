# Valkyrie Utils

Valkyrie Utils is a Python utility library that provides convenient and flexible functionalities through its four main modules: Logger, Config, Tools, and Options.

## Table of Contents

- [About](#about)
- [Usage](#usage)
- [Modules](#modules)
  - [Logger](#valkyrie-logger)
  - [Config](#valkyrie-config)
  - [Tools](#valkyrie-tools)
  - [Options](#valkyrie-options)
- [Example Usage](#example-usage)

## About

This utility library was created to demonstrate how to use ValkyrieUtils modules in Python applications. The modules offer functionality to handle logging, configuration, data validation, and command-line options efficiently.

## Usage

To use Valkyrie Utils, you'll need to import the desired module(s) into your Python script and follow the provided guidelines and examples. Here's a brief overview of each module:

- **Logger**: Facilitates easy logging with configurable log levels and file handling.
- **Config**: Enables easy reading and parsing of configuration files (both INI and XML).
- **Tools**: Provides functions to validate various data types (e.g., float, integer, boolean, list, dictionary).
- **Options**: Allows you to define and parse command-line options with specified data types and default values.

## Modules

### Valkyrie Logger

The Logger module (`Logger.py`) provides a flexible logging solution for Python applications. It allows you to set the log level, define log file paths, and toggle debug mode.
> - Refer to the [Valkyrie Logger documentation](./readme/logger.md) for more information.

### Valkyrie Config

The Config module (`Config.py`) facilitates reading and parsing configuration files, supporting both INI and XML formats. It provides methods to extract configuration values in various data types.
> - Refer to the [Valkyrie Config documentation](./readme/config.md) for more information.

### Valkyrie Tools

The Tools module (`Tools.py`) offers functions to validate different data types, such as float, integer, boolean, list, and dictionary. It also includes a function to match dictionary values to their appropriate data types.
> - Refer to the [Valkyrie Tools documentation](./readme/tools.md) for more information.

### Valkyrie Options

The Options module (`Options.py`) helps manage command-line options by allowing easy definition of options with specified data types, help messages, and default values. It provides a way to parse and access these options within your script.
> - Refer to the [Valkyrie Options documentation](./readme/options.md) for more information.

## Example Usage

```python
# Example usage of ValkyrieUtils modules
# Run this script with the following command: python ValkyrieUtils.py --config_file example.xml

from Logger import ValkyrieLogger
from Config import ValkyrieConfig
from Tools import ValkyrieTools
from Options import ValkyrieOptions

def run_test(debug):
    # ... (rest of the example script)

if __name__ == '__main__':
    run_test(debug=False)
```

The above example showcases how to utilize ValkyrieUtils modules in a Python script. Modify the `run_test` function as needed to suit your application's requirements.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

