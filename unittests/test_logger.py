import unittest
from Logger import ValkyrieLogger


class TestValkyrieLogger(unittest.TestCase):

    def test_info(self):
        # Test info log
        logger = ValkyrieLogger('info')
        logger.info("Info log message")

    def test_debug(self):
        # Test debug log
        logger = ValkyrieLogger('debug')
        logger.debug("Debug log message")

    def test_error(self):
        # Test error log
        logger = ValkyrieLogger('error')
        logger.error("Error log message")

    def test_console(self):
        # Test console log
        logger = ValkyrieLogger('info')
        logger.console('info', 'Console info log message')

    def test_console_error(self):
        # Test console error log
        logger = ValkyrieLogger('error')
        logger.consoleError('Console error log message')


if __name__ == '__main__':
    unittest.main()
