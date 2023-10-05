import unittest
from Compressor import ValkyrieCompressor

class TestValkyrieCompressor(unittest.TestCase):

    def test_deflate_inflate_gzip(self):
        data = b"Sample data to be compressed"
        compressed_data = ValkyrieCompressor.deflate(data, 'gzip')
        decompressed_data = ValkyrieCompressor.inflate(compressed_data, 'gzip')
        self.assertEqual(data, decompressed_data)

    def test_deflate_inflate_bzip2(self):
        data = b"Sample data to be compressed"
        compressed_data = ValkyrieCompressor.deflate(data, 'bzip2')
        decompressed_data = ValkyrieCompressor.inflate(compressed_data, 'bzip2')
        self.assertEqual(data, decompressed_data)

    def test_deflate_inflate_lzma(self):
        data = b"Sample data to be compressed"
        compressed_data = ValkyrieCompressor.deflate(data, 'lzma')
        decompressed_data = ValkyrieCompressor.inflate(compressed_data, 'lzma')
        self.assertEqual(data, decompressed_data)
        
    def test_deflate_inflate_lz4(self):
        data = b"Sample data to be compressed"
        compressed_data = ValkyrieCompressor.deflate(data, 'lz4')
        decompressed_data = ValkyrieCompressor.inflate(compressed_data, 'lz4')
        self.assertEqual(data, decompressed_data)
        
    def test_deflate_inflate_zstd(self):
        data = b"Sample data to be compressed"
        compressed_data = ValkyrieCompressor.deflate(data, 'zstd')
        decompressed_data = ValkyrieCompressor.inflate(compressed_data, 'zstd')
        self.assertEqual(data, decompressed_data)
        
    def test_deflate_inflate_none(self):
        data = b"Sample data to be compressed"
        compressed_data = ValkyrieCompressor.deflate(data, 'none')
        decompressed_data = ValkyrieCompressor.inflate(compressed_data, 'none')
        self.assertEqual(data, decompressed_data)


if __name__ == '__main__':
    unittest.main()
