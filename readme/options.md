## Valkyrie Options Module

The Options module (`Options.py`) provides a configurable command-line option parser using `OptionParser`. It allows easy definition of options with specified data types, help messages, and default values. The parsed options can be accessed through a dictionary-like interface.

### Usage

1. Import the Options module into your Python script.
2. Define the options using the `ValkyrieOptions` class by providing tuples for each option.
3. Parse the command-line arguments and access the parsed options through a dictionary-like interface.

### Example

```python
from Options import ValkyrieOptions

# Initialize Valkyrie Command Line Options
options_parser = ValkyrieOptions([
    ('server_id', 'int', 'Server ID'),
    ('config_file', 'str', 'Configuration File Path and filename', 'valkyrie.conf')
])

# Add more options after initializing
options_parser.add_option([
    ('log_level', 'str', 'Log writing level'),
    ('log_file', 'str', 'Log path(absolute) and file name')
])

# Parse the given Command Line Options
parsed_options = options_parser.parse()

# Print the parsed options
print(parsed_options.keys(), parsed_options)
print(parsed_options['server_id'])
print(parsed_options.config_file)
```
In this example, we define two options, `server_id` and `config_file`, with specified data types, help messages, and 
default values. We then parse the command-line arguments and access the parsed options through a dictionary-like 
interface.

### Unit Tests

The ValkyrieOptions module includes unit tests to ensure that the module is working as intended. To run the unit tests,
run the following command in the root directory of the project:

```bash
python -m unittest unittests/test_options.py
```

### Supported Classes and Functions

- `ValkyrieOptions`: A class to manage command-line options and configuration. It uses `OptionParser` to handle command-line options.
    - `__init__(*options)`: Initialize the option parser.
    - `add_option(*options)`: Add a new option to the parser.
    - `parse(args=None)`: Parse the command-line arguments.
- `CmdOptions`: A class to manage configuration options. It is a subclass of `dict`, allowing access to options like a dictionary.
