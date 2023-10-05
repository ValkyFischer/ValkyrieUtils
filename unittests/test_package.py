import unittest
import logging
from unittest.mock import MagicMock
from Crypto import ValkyrieCrypto
from Package import ValkyriePackage

class TestValkyriePackage(unittest.TestCase):

    def setUp(self):
        _key = '0123456789abcdef0123456789abcdef'
        _iv = '0123456789abcdef'
        self.key = ValkyrieCrypto.generate_argon_key(_key, _iv)
        # Create a mock logger for testing
        self.logger = logging.getLogger("ValkyriePackage")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

    def test_info(self):
        # Create a ValkyriePackage instance
        vpk = ValkyriePackage(self.key)

        # Define expected header data
        expected_header = {
            'filename': 'example',
            'fileinfo': 'Encrypted data package',
            'filesize': 2203923,
            'author': 'Valky Fischer',
            'copyright': 'Valky ⓒ 2023',
            'timestamp': 1696440810,
            'encryption': 'AES-GCM',
            'key_length': 32,
            'version': 2,
            'compression': 'zstd'
        }

        # Mock the open function to return the header data
        # with unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data=b'header_data')) as m:
        try:
            vpk.read(r"../examples/example.vpk")
            result = vpk.info('../examples/example.vpk')
        except Exception as e:
            vpk.read(r"examples/example.vpk")
            result = vpk.info('examples/example.vpk')

        # Check if the result matches the expected header data
        self.assertDictEqual(result, expected_header)

    def test_read(self):
        # Create a ValkyriePackage instance
        vpk = ValkyriePackage(self.key, logger=self.logger, debug=True)

        # Mock the _read_vpk, _decompress, and _decrypt methods
        vpk._read_vpk = MagicMock(return_value=b'compressed_data')
        vpk._decompress = MagicMock(return_value=b'encrypted_data')
        vpk._decrypt = MagicMock(return_value={'file1.txt': b'file_data'})
        vpk._check = MagicMock(return_value=True)

        # Call the read method
        result = vpk.read('example.vpk')

        # Check if the result is correct
        expected_result = {'file1.txt': b'file_data'}
        self.assertDictEqual(result, expected_result)

    def test_create(self):
        # Create a ValkyriePackage instance
        vpk = ValkyriePackage(self.key, logger=self.logger, debug=True)

        # Mock the _read_dir and _save methods
        vpk._read_dir = MagicMock(return_value={'file1.txt': b'file_data'})
        vpk._save = MagicMock(return_value='output.vpk')

        # Call the create method
        result = vpk.create('/path/to/directory', 'output.vpk')

        # Check if the result is correct
        expected_result = 'output.vpk'
        self.assertEqual(result, expected_result)
        
    def test_update(self):
        # Create a ValkyriePackage instance
        vpk = ValkyriePackage(self.key, logger=self.logger, debug=True)

        # Mock the _read_dir and _save methods
        vpk.read = MagicMock(return_value={'file1.txt': b'file_data'})
        vpk.save = MagicMock(return_value='output.vpk')

        # Call the create method
        result = vpk.update({'file2.txt': b'file_data'}, 'output.vpk')

        # Check if the result is correct
        expected_result = 'output.vpk'
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
