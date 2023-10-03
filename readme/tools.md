## Valkyrie Tools Module

The Tools module (`Tools.py`) provides utility functions within the `ValkyrieTools` class to check and match various types of input. It can determine if an object can be interpreted as a float, integer, boolean, list, or dictionary. Additionally, it offers a function to match a dictionary's values to their correct data types based on these types.

### Usage

1. Import the Tools module into your Python script.
2. Use the provided functions (`isFloat`, `isInteger`, `isBoolean`, `isList`, `isDict`, `matchDict`) to check and match input values.
3. Use the provided functions (`formatSize`, `formatSpeed`, `formatTime`, `generateHwid`, `generateCode`, `markdownHtml`, `getHash`, `getFileHash`, `getFileSize`, `getFileList`) to format data, generate unique IDs, and get file information.

### Example

```python
from Tools import ValkyrieTools

# Check types
print(ValkyrieTools.isList([1, 2, 3]))  # True
print(ValkyrieTools.isList({'a': 1, 'b': 2}))  # False
print(ValkyrieTools.isDict({'a': 1, 'b': 2}))  # True
print(ValkyrieTools.isBoolean('True'))  # True
print(ValkyrieTools.isBoolean('False'))  # True
print(ValkyrieTools.isBoolean('Maybe'))  # False
print(ValkyrieTools.isFloat('1.0'))  # True
print(ValkyrieTools.isFloat(1))  # False
print(ValkyrieTools.isInteger(1))  # True
print(ValkyrieTools.isInteger(1.3))  # False

# Match dictionary values to correct types
test_dict = {
    "a": "1", "b": "2", "c": "3", "d": "True", "e": "False", "f": "Yes", "g": "No",
    "h": "1.3", "i": "1.0", "j": "5", "k": "Maybe", "l": "[1, 2, 3]", "m": "{'a': 1, 'b': 2}"
}
print(ValkyrieTools.matchDict(test_dict))

# Get unique hardware ID
print(ValkyrieTools.generateHwid())

# Markdown formatting
print(ValkyrieTools.markdownHtml('**Hello** *world*!'))
```

In this example, we demonstrate how to use the `ValkyrieTools` module to check and match various types of input. 
We also showcase the ability to generate a unique hardware ID and format Markdown text to HTML.

### Supported Classes and Functions

- `ValkyrieTools`: A class to provide utility functions.
    - `isFloat(obj)`: Check if the input can be parsed as a float.
    - `isInteger(obj)`: Check if the input can be parsed as an integer.
    - `isBoolean(obj)`: Check if the input represents a boolean value.
    - `isList(obj)`: Check if the input is a list.
    - `isDict(obj)`: Check if the input is a dictionary.
    - `isJson(obj)`: Check if the input is a valid JSON string.
    - `matchDict(obj)`: Match the input dictionary to the correct type.
    - `formatSize(size)`: Format the input size (in bytes) to a human-readable format.
    - `formatSpeed(speed)`: Format the input speed (in bits) to a human-readable format.
    - `formatTime(time)`: Format the input time (in seconds) to a human-readable format.
    - `generateHwid()`: Generate a unique hardware ID for the current machine.
    - `generateCode(length)`: Generate a random code of the specified length.
    - `markdownHtml(text)`: Convert the input Markdown text to HTML.
    - `getHash(data, hash_type)`: Get the hash of the input data.
    - `getFileHash(file_path, hash_type, buffer)`: Get the hash of the input file.
    - `getFileSize(file_path)`: Get the size of the input file.
    - `getFileList(path)`: Get a list of all files in the directories.

---

#### Note

For the `matchDict` function, it identifies and matches the following types:
- Integer
- Float
- Boolean
- List
- Dictionary

*Any value that doesn't match these types is treated as a string.*
