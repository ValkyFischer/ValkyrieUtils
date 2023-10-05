import unittest
import tempfile
import os
from unittest.mock import patch
from Manifest import ValkyrieManifest

class TestValkyrieManifest(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_folder = self.temp_dir.split('\\')[-1]
        self.manifest_file = os.path.join(self.temp_dir, "manifest.json")
        self.manifest = ValkyrieManifest(self.temp_dir, (self.temp_dir, "manifest"), False)

    def test_downloadFile(self):
        # Mock urllib.request.urlretrieve
        with patch("urllib.request.urlretrieve") as mock_urlretrieve:
            file_path = "example_file.txt"
            remote_url = "http://example.com/files"

            # Call the method
            self.manifest.dir = self.temp_dir
            result = self.manifest.downloadFile(file_path, remote_url)

            # Check if urllib.request.urlretrieve was called with the correct arguments
            mock_urlretrieve.assert_called_once_with(f"{remote_url}/{file_path}", self.temp_dir.replace(f"\\{self.temp_folder}", "") + "\\" + file_path)

            # Check the result
            self.assertTrue(result)

    def test_checkFile(self):
        # Create a dummy file
        file_path = "dummy_file.txt"
        dummy_file = os.path.join(self.temp_dir, file_path)
        with open(dummy_file, "w") as f:
            f.write("dummy content")

        # Hash the dummy file
        hash_dict = self.manifest.getHash([dummy_file])
        
        # Check the file
        result = self.manifest.checkFile(file_path, hash_dict[dummy_file])
        
        # Check the result
        self.assertTrue(result)
        
    def test_createManifest(self):
        # Create a dummy file
        file_path = "dummy_file.txt"
        dummy_file = os.path.join(self.temp_dir, file_path)
        with open(dummy_file, "w") as f:
            f.write("dummy content")

        # Create the manifest
        self.manifest.createManifest()

        # Check the result
        self.assertTrue(os.path.exists(self.manifest_file))


if __name__ == "__main__":
    unittest.main()
