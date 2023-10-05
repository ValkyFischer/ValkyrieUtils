import os
import tempfile
import time
import unittest
from Tools import ValkyrieTools

class TestTools(unittest.TestCase):
    def test_isFloat(self):
        self.assertTrue(ValkyrieTools.isFloat('1.0'))
        self.assertFalse(ValkyrieTools.isFloat(1))

    def test_isInteger(self):
        self.assertTrue(ValkyrieTools.isInteger(1))
        self.assertFalse(ValkyrieTools.isInteger(1.3))

    def test_isBoolean(self):
        self.assertTrue(ValkyrieTools.isBoolean('True'))
        self.assertTrue(ValkyrieTools.isBoolean('False'))
        self.assertTrue(ValkyrieTools.isBoolean('Yes'))
        self.assertTrue(ValkyrieTools.isBoolean('No'))
        self.assertFalse(ValkyrieTools.isBoolean('1'))
        self.assertFalse(ValkyrieTools.isBoolean('0'))
        self.assertTrue(ValkyrieTools.isBoolean(1))
        self.assertTrue(ValkyrieTools.isBoolean(0))
        self.assertFalse(ValkyrieTools.isBoolean('Maybe'))

    def test_isList(self):
        self.assertTrue(ValkyrieTools.isList([1, 2, 3]))
        self.assertFalse(ValkyrieTools.isList({'a': 1, 'b': 2}))

    def test_isDict(self):
        self.assertTrue(ValkyrieTools.isDict({'a': 1, 'b': 2}))
        self.assertFalse(ValkyrieTools.isDict([1, 2, 3]))

    def test_isJson(self):
        self.assertTrue(ValkyrieTools.isJson('{"key": "value"}'))
        self.assertFalse(ValkyrieTools.isJson('invalid_json'))

    def test_matchDict(self):
        test_dict = {
            "a": "1", "b": "2", "c": "3", "d": "True", "e": "false", "f": "Yes", "g": "NO",
            "h": "1.3", "i": "1.0", "j": "5", "k": "Maybe", "l": "[1, 2, 3]", "m": "{'a': 1, 'b': 2}"
        }
        expected_result = {'a': 1, 'b': 2, 'c': 3, 'd': True, 'e': False, 'f': True, 'g': False,
                            'h': 1.3, 'i': 1.0, 'j': 5, 'k': 'Maybe', 'l': [1, 2, 3], 'm': {'a': 1, 'b': 2}}
        self.assertEqual(ValkyrieTools.matchDict(test_dict), expected_result)

    def test_formatSize(self):
        self.assertEqual(ValkyrieTools.formatSize(1000000000), '1.00 GB')
        self.assertEqual(ValkyrieTools.formatSize(1000000), '1.00 MB')
        self.assertEqual(ValkyrieTools.formatSize(1000), '1.00 KB')
        self.assertEqual(ValkyrieTools.formatSize(500), '500.00 B')

    def test_formatSpeed(self):
        self.assertEqual(ValkyrieTools.formatSpeed(1000000), '1.00 MB/s')
        self.assertEqual(ValkyrieTools.formatSpeed(1000), '1.00 KB/s')
        self.assertEqual(ValkyrieTools.formatSpeed(500), '500.00 B/s')
    
    def test_formatTime(self):
        self.assertEqual(ValkyrieTools.formatTime(1000000), '11.57 days')
        self.assertEqual(ValkyrieTools.formatTime(3600), '1.00 hours')
        self.assertEqual(ValkyrieTools.formatTime(120), '2.00 minutes')
        self.assertEqual(ValkyrieTools.formatTime(30), '30.00 seconds')
    
    def test_formatNumber(self):
        self.assertEqual(ValkyrieTools.formatNumber(1234567.89), '1,234,567.89')
    
    def test_generateHwid(self):
        # As this function generates a unique hardware ID, it's difficult to test for a specific result.
        # You can verify that it returns a non-empty string, for example.
        hwid = ValkyrieTools.generateHwid()
        self.assertTrue(hwid)
    
    def test_generateCode(self):
        code_length = 32
        generated_code = ValkyrieTools.generateCode(code_length)
        self.assertEqual(len(generated_code), code_length)
    
    def test_markdownHtml(self):
        markdown_text = '**Hello** *World*!'
        expected_html = '<b>Hello</b> <i>World</i>!'
        self.assertEqual(ValkyrieTools.markdownHtml(markdown_text), expected_html)
    
    def test_getHash(self):
        data = b'This is some data to hash'
        expected_md5_hash = 'fbe8ee5bbfd9ec0c6f1949ba2ac9e0d7'
        expected_sha1_hash = '6acc0ca14c9cd14671c1034a36396066c00ad053'
        expected_sha256_hash = '09b0d6cdcb1dc978740a4510cfbce9308423817d78447a7345bafc2950c8ff7b'
        expected_sha512_hash = '6b0e3ed391e918823f5faf249c3e077ad9f5681d1d9b6c19f4e669caae3d8abefbf0bb9d443150ab62632e69554d0d22ae6be9c70334005ba0566bd6c2eff822'
        self.assertEqual(ValkyrieTools.getHash(data, 'md5'), expected_md5_hash)
        self.assertEqual(ValkyrieTools.getHash(data, 'sha1'), expected_sha1_hash)
        self.assertEqual(ValkyrieTools.getHash(data, 'sha256'), expected_sha256_hash)
        self.assertEqual(ValkyrieTools.getHash(data, 'sha512'), expected_sha512_hash)
    
    def test_getFileHash(self):
        file_content = "This is the file content."
        temp_path = tempfile.gettempdir()
        temp_file = tempfile.NamedTemporaryFile(dir=temp_path, delete=False)
        temp_file.write(file_content.encode('utf-8'))
        temp_file.close()
        
        expected_md5_hash = '066f587e2cff2588e117fc51a522c47e'
        expected_sha1_hash = '7a2dc28ce65f9b346523bd0e2f177d3b7357aba1'
        expected_sha256_hash = 'dc9dbf28907435fb339baac4eb2b386538570c20ba1fcd3373f9c24d95a84ff4'
        expected_sha512_hash = 'b345bc4c99404c161d67793aa412d8120a9831cfa4f307a8e8b8b290530665b17675106f5d6eebfdc0a82e43d2d4207a6485d5ff8d8dc124d0e20681d150a609'
        
        self.assertEqual(ValkyrieTools.getFileHash(temp_file.name, 'md5'), expected_md5_hash)
        self.assertEqual(ValkyrieTools.getFileHash(temp_file.name, 'sha1'), expected_sha1_hash)
        self.assertEqual(ValkyrieTools.getFileHash(temp_file.name, 'sha256'), expected_sha256_hash)
        self.assertEqual(ValkyrieTools.getFileHash(temp_file.name, 'sha512'), expected_sha512_hash)
        
    def test_getFileData(self):
        file_content = b'This is the file content.'
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        self.assertEqual(ValkyrieTools.getFileData(temp_file_path), file_content)

    def test_getFileSize(self):
        file_content = b'This is the file content.'
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
            expected_file_size = len(file_content)
        self.assertEqual(ValkyrieTools.getFileSize(temp_file_path), expected_file_size)

    def test_getFileEdit(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
            time.sleep(1)
            expected_edit_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(temp_file_path)))
            self.assertEqual(ValkyrieTools.getFileEdit(temp_file_path), expected_edit_time)

    def test_getFileList(self):
        temp_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(temp_dir, 'subdir'))
        with tempfile.NamedTemporaryFile(dir=temp_dir) as temp_file1:
            with tempfile.NamedTemporaryFile(dir=os.path.join(temp_dir, 'subdir')) as temp_file2:
                expected_file_list = [temp_file1.name.replace("\\", "/"), temp_file2.name.replace("\\", "/")]
                self.assertEqual(ValkyrieTools.getFileList(temp_dir), expected_file_list)


if __name__ == '__main__':
    unittest.main()
