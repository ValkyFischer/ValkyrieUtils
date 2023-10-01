## Valkyrie Config Module

The Config module (`Config.py`) provides a versatile configuration reader for INI and XML files. It allows users to easily read and retrieve configuration values from these file formats. The supported operations include fetching values as strings, integers, floats, booleans, and dictionaries, allowing for flexible usage based on the configuration file type.

### Usage

1. Import the Config module into your Python script.
2. Initialize a configuration reader instance using `ValkyrieConfig` with the absolute path to the configuration file.
3. Use the provided functions (`get_string`, `get_int`, `get_boolean`, `get_float`, `get_value`, `get_dict`, `get_config`) to read configuration values.

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
```

In this example, we demonstrate how to read configuration values from both INI and XML files using the Config module.

### Supported Operations

- `get_string(section, key, default=None)`: Get a string value from the configuration.
- `get_int(section, key, default=None)`: Get an integer value from the configuration.
- `get_boolean(section, key, default=None)`: Get a boolean value from the configuration.
- `get_float(section, key, default=None)`: Get a float value from the configuration.
- `get_value(node, default=None)`: Get a value from the configuration.
- `get_dict(section)`: Get a full section as a dictionary from the configuration.
- `get_config()`: Get the complete configuration as a dictionary.

### File Formats

The module supports reading configuration from both INI and XML file formats.

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
    <Test1 version="test_0.1" order="1" value="test_key_xml" />
    <Test2 name="test_xml" order="2" value="2000">DataXML</Test2>
</Config>
```

### Note

For any unsupported file format or operations, appropriate exceptions are raised.
