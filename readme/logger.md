## Valkyrie Logger Module

The Logger module (`Logger.py`) provides a flexible logging utility for creating log messages with various log levels, including info, debug, warning, error, and critical. It offers the ability to direct log messages to both a log file and/or the console. The module also supports formatting log messages with caller information and customizable message components.

### Usage

1. Import the Logger module into your Python script.
2. Initialize a logger instance using `ValkyrieLogger`.
3. Use the logging functions (`Info`, `Debug`, `Error`, `Console`, `ConsoleError`) to log messages at different levels.

### Example

```python
from Logger import ValkyrieLogger

# Initialize a logger instance
log = ValkyrieLogger('info', '.\\log\\logger.log', 'ValkyrieLogger', True)

# Log various messages
log.info(1, 1, 'val1,%s,val2,%s' % (10, 20))
log.info(1, 2, 'val1', 10, 'val2', 20)
log.info('# This is a test message')

log.debug(1, 1, val1 = 10, val2 = 20)
log.error('# This is an error message', val1 = 10, val2 = 20)

# Log to the console
log.console('info', '# This is an info message')
log.console('debug', '# This is a debug message')

# Log an error to the console
log.consoleError('# This is an error message')
```

In this example, we create a logger with the `info` log level, directing log messages to both a log file and the 
console. We then log various messages using different log functions.

### Unit Tests

The ValkyrieLogger module includes unit tests to ensure that the module is working as intended. To run the unit tests,
run the following command in the root directory of the project:

```bash
python -m unittest unittests/test_logger.py
```

### Supported Classes and Functions

- `ValkyrieLogger`: A class to create a logger instance.
    - `__init__(log_level='info', log_file=None, app_name=None, debug_mode=False)`: Initialize a logger instance.
    - `Info(*args, **kwargs)`: Log an info message.
    - `Debug(*args, **kwargs)`: Log a debug message.
    - `Error(*args, **kwargs)`: Log an error message.
    - `Console(msg_type, *args, **kwargs)`: Log a message to the console.
    - `ConsoleError(*args, **kwargs)`: Log an error message to the console.

### Supported Log Levels

- `DEBUG`: Detailed information, typically useful for debugging.
- `INFO`: Informational messages regarding the progress of the application.
- `WARNING`: Indication that something unexpected happened or an issue might arise soon.
- `ERROR`: Indicates a more serious issue or error in the application.
- `CRITICAL`: A very serious error that may prevent the program from continuing.

### Customization

The Logger module allows customization of log levels, log file paths, application names, and the ability to include caller information in log messages. You can tailor the log configuration to suit the specific needs of your application.
