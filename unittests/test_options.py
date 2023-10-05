import unittest
from Options import ValkyrieOptions, CmdOptions

class TestValkyrieOptions(unittest.TestCase):

    def test_add_option(self):
        # Initialize ValkyrieOptions
        options_parser = ValkyrieOptions()
        
        # Check initially no options
        self.assertEqual(len(options_parser._parser.option_list), 1)

        # Add an option
        options_parser.add_option([('server_id', 'int', 'Server ID', 1)])
        self.assertEqual(len(options_parser._parser.option_list), 2)

        # Add multiple options
        options_parser.add_option([
            ('config_file', 'str', 'Configuration File Path and filename', 'valkyrie.conf'),
            ('log_level', 'str', 'Log writing level', 'info')
        ])
        self.assertEqual(len(options_parser._parser.option_list), 4)

    def test_parse(self):
        # Initialize ValkyrieOptions
        args = [
            ('server_id',   'int', 'Server ID', 42),
            ('config_file', 'str', 'Configuration File Path and filename', 'valkyrie.conf')
        ]
        options_parser = ValkyrieOptions(args)

        # Parse the arguments
        parsed_options = options_parser.parse()

        # Check parsed options
        self.assertEqual(parsed_options['server_id'], 42)
        self.assertEqual(parsed_options.config_file, 'valkyrie.conf')

    def test_CmdOptions(self):
        # Create a CmdOptions instance
        cmd_options = CmdOptions({'server_id': 1, 'config_file': 'valkyrie.conf'})

        # Test accessing options
        self.assertEqual(cmd_options['server_id'], 1)
        self.assertEqual(cmd_options.config_file, 'valkyrie.conf')

        # Test accessing non-existent option
        self.assertIsNone(cmd_options.get('nonexistent_option'))
        self.assertIsNone(cmd_options.nonexistent_option)


if __name__ == "__main__":
    unittest.main()
