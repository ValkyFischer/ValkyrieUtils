## Valkyrie Config Module

The Config module (`Config.py`) provides a versatile configuration reader for INI, XML, JSON and VCF files. 
It allows users to easily read and retrieve configuration values from these file formats. 
The supported operations include fetching values as strings, integers, floats, booleans, and dictionaries, allowing for flexible usage based on the configuration file type. 
VCF files are a custom file format designed for encrypted configuration files.

### Usage

1. Import the Config module into your Python script.
2. Initialize a configuration reader instance using `ValkyrieConfig` with the absolute path to the configuration file.
3. Use the provided functions (`get_string`, `get_int`, `get_boolean`, `get_float`, `get_value`, `get_dict`, `get_config` and `save`) to read and save configuration values.

### Example

```python
from Config import ValkyrieConfig

# Initialize a configuration reader instance for INI file
config_ini = ValkyrieConfig("example.ini")
# Read values from INI file
print(config_ini.get_string('Test1', 'value'))  # 'test_key_ini'
print(config_ini.get_int('Test2', 'value'))     # 1000
print(config_ini.get_config())


# Initialize a configuration reader instance for XML file
config_xml = ValkyrieConfig("example.xml")
# Read values from XML file
print(config_xml.get_string("Test1", "value"))  # 'test_key_xml'
print(config_xml.get_int("Test2", "value"))     # 2000
print(config_xml.get_config())


# Initialize a configuration reader instance for JSON file
config_json = ValkyrieConfig("example.json")
# Read values from JSON file
print(config_json.get_string("Test1", "value"))  # 'test_key_json'
print(config_json.get_int("Test2", "value"))     # 3000
print(config_json.get_config())
```

In this example, we demonstrate how to read configuration values from `INI`, `XML`, `JSON` and `VCF` files using the Config module.

### Supported Classes and Functions
- `ValkyrieConfig`: A class to read configuration from INI, XML and JSON files.
    - `__init__(file)`: Initialize a configuration reader instance.
    - `get_string(section, key, default=None)`: Get a string value from the configuration.
    - `get_int(section, key, default=None)`: Get an integer value from the configuration.
    - `get_boolean(section, key, default=None)`: Get a boolean value from the configuration.
    - `get_float(section, key, default=None)`: Get a float value from the configuration.
    - `get_value(node, default=None)`: Get a value from the configuration. XML only.
    - `get_dict(section)`: Get a full section as a dictionary from the configuration.
    - `get_config()`: Get the complete configuration as a dictionary.
    - `save(config, file=None)`: Save the configuration to a file.

### File Formats

The module supports reading configuration from the following file formats:
- `INI`: A configuration file format that stores data in a key-value pair format.
- `XML`: A configuration file format that stores data in a tree structure.
- `JSON`: A configuration file format that stores data in a key-value pair format.
- `VCF`: An encrypted configuration file format that stores data in a key-value pair format.

### Configuration File Examples

#### example.ini

```ini
[Test1]
value=test_key_ini
version=test_0.1
order=1

[Test2]
value=1000
name=test_ini
order=2
```

#### example.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Config>
    <Test1 version="test_0.2" order="1" value="test_key_xml" />
    <Test2 name="test_xml" order="2" value="2000">DataXML</Test2>
</Config>
```

#### example.json

```json
{
    "Test1": {
        "version": "test_0.3",
        "order": 1,
        "value": "test_key_json"
    },
    "Test2": {
        "name": "test_json",
        "order": 2,
        "value": 3000
    }
}
```

#### example.vcf

```vcf
{
    "ciphertext": "7b297a9c3494a387f327423b27437sd8f58sdft87dsfz8rzn3849n84wrfrn834mrzc8734nrgh8vn3487rcf34c03622b19a7f2bd761e452478839189b50bd84bcb010cf11735834c84ba18ed7e270c4154133c25634f55144f79b2e38cf26303b78f0ad85dde533a75abdeefc821469782cd45879aa1b3dcd53ccae1bda0254919e482a17c0fbe10f0e",
    "tag": "0ae13e1cce43870c60ffaa687b7f1339",
    "iv": "08d9b22ea08c0ef8bd0a2b39d3c612f6"
}
```

### Note

For any unsupported file format or operations, appropriate exceptions are raised.
