
## Valkyrie Tools Module

The Tools module (`Tools.py`) provides utility functions within the `ValkyrieTools` class to check and match various types of input. It can determine if an object can be interpreted as a float, integer, boolean, list, or dictionary. Additionally, it offers a function to match a dictionary's values to their correct data types based on these types.

### Usage

1. Import the Tools module into your Python script.
2. Use the provided functions (`isFloat`, `isInteger`, `isBoolean`, `isList`, `isDict`, `matchDict`) to check and match input values.

### Example

```python
from Tools import ValkyrieTools

# Check types
print(ValkyrieTools.isList([1, 2, 3]))  # True
print(ValkyrieTools.isList({'a': 1, 'b': 2}))  # False
print(ValkyrieTools.isDict({'a': 1, 'b': 2}))  # True
print(ValkyrieTools.isBoolean('True'))  # True
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
# Returns {'a': 1, 'b': 2, 'c': 3, 'd': True, 'e': False, 'f': True, 'g': False,
#          'h': 1.3, 'i': 1.0, 'j': 5, 'k': 'Maybe', 'l': [1, 2, 3], 'm': {'a': 1, 'b': 2}}
```

### Supported Functions

- `isFloat(obj)`: Check if the input can be parsed as a float.
- `isInteger(obj)`: Check if the input can be parsed as an integer.
- `isBoolean(obj)`: Check if the input represents a boolean value.
- `isList(obj)`: Check if the input is a list.
- `isDict(obj)`: Check if the input is a dictionary.
- `matchDict(obj)`: Match the input dictionary to the correct type.

### Note

For the `matchDict` function, it identifies and matches the following types:
- Integer
- Float
- Boolean
- List
- Dictionary

Any value that doesn't match these types is treated as a string.
