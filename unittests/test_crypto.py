import unittest
from Crypto import ValkyrieCrypto, AES_GCM, AES_CTR

class TestValkyrieCrypto(unittest.TestCase):
    
    def setUp(self):
        key = '0123456789abcdef0123456789abcdef'
        iv = '0123456789abcdef'
        self.key = ValkyrieCrypto.generate_argon_key(key, iv)
        self.plaintext = b'Hello, World!'
    
    def test_argon_key(self):
        self.assertEqual(len(self.key), 32)

    def test_encrypt_decrypt_aes_gcm(self):
        encrypted_data = ValkyrieCrypto.encrypt_data(self.key, self.plaintext, mode=AES_GCM)
        decrypted_data = ValkyrieCrypto.decrypt_data(self.key, encrypted_data, mode=AES_GCM)

        self.assertEqual(self.plaintext, decrypted_data.encode('utf-8'))

    def test_encrypt_decrypt_aes_ctr(self):
        encrypted_data = ValkyrieCrypto.encrypt_data(self.key, self.plaintext, mode=AES_CTR)
        decrypted_data = ValkyrieCrypto.decrypt_data(self.key, encrypted_data, mode=AES_CTR)

        self.assertEqual(self.plaintext, decrypted_data.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
