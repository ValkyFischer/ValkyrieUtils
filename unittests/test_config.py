import os.path
import unittest
from time import sleep
from unittest.mock import patch
from Config import ValkyrieConfig

class TestValkyrieConfig(unittest.TestCase):

    def setUp(self):
        try:
            self.config_ini = ValkyrieConfig("../examples/example.ini")
            self.config_xml = ValkyrieConfig("../examples/example.xml")
            self.config_json = ValkyrieConfig("../examples/example.json")
            self.out = "../examples/out/example_out.ini"
        except Exception as e:
            self.config_ini = ValkyrieConfig("examples/example.ini")
            self.config_xml = ValkyrieConfig("examples/example.xml")
            self.config_json = ValkyrieConfig("examples/example.json")
            self.out = "examples/out/example_out.ini"

    def test_get_string_ini(self):
        self.assertEqual(self.config_ini.get_string('Test1', 'value'), 'test_key_ini')

    def test_get_int_ini(self):
        self.assertEqual(self.config_ini.get_int('Test2', 'value'), 1000)

    def test_get_string_xml(self):
        self.assertEqual(self.config_xml.get_string('Test1', 'value'), 'test_key_xml')

    def test_get_int_xml(self):
        self.assertEqual(self.config_xml.get_int('Test2', 'value'), 2000)

    def test_get_string_json(self):
        self.assertEqual(self.config_json.get_string('Test1', 'value'), 'test_key_json')

    def test_get_int_json(self):
        self.assertEqual(self.config_json.get_int('Test2', 'value'), 3000)

    def test_invalid_value(self):
        self.assertFalse(self.config_ini.get_string('Test1', 'invalid_key'))

    @patch('Config.ValkyrieConfig.get_config')
    def test_save(self, mock_get_config):
        mock_get_config.return_value = {'Test1': {'value': 'test_key_ini'}, 'Test2': {'value': 1000}}
        self.config_ini.save(self.config_ini.get_config(), self.out)
        sleep(1)
        self.assertTrue(os.path.exists(self.out))


if __name__ == '__main__':
    unittest.main()
