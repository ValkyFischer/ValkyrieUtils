## Valkyrie Crypto Module

### Table of Contents

- [Valkyrie Crypto Module](#valkyrie-crypto-module)
    - [Table of Contents](#table-of-contents)
    - [About](#about)
    - [Usage](#usage)
    - [Example](#example)
    - [Unit Tests](#unit-tests)
    - [Supported Classes and Functions](#supported-classes-and-functions)
    - [Supported Encryption Modes](#supported-encryption-modes)

### About

The Crypto module (`Crypto.py`) provides functions to encrypt and decrypt data using AES-GCM, AES-CTR, and AES-CBC. 
Additionally, it offers a function to generate a key using Argon2, a memory-hard function designed to be resistant 
to GPU cracking attacks. The module is designed to simplify the encryption and decryption of data by providing
ready-to-use functions for common encryption modes. 

### Usage

1. Import the Crypto module into your Python script.
2. Use the `ValkyrieCrypto` class to perform encryption, decryption, and key generation.
3. Choose a suitable encryption mode and call the respective functions to encrypt and decrypt data.
4. Generate a key using Argon2 for secure encryption and decryption.

### Example

```python
from Crypto import ValkyrieCrypto

# Test the encrypt_data and decrypt_data functions
sample_key = '0123456789abcdef0123456789abcdef'
sample_iv = '0123456789abcdef'
bytes_data = b'Hello, World!'
print('Byte-like data:', bytes_data)

# Generate a key using Argon2
encryption_key = ValkyrieCrypto.generate_argon_key(sample_key, sample_iv)
print('Encryption key:', encryption_key)

# Encrypt the plaintext
encryption_data = ValkyrieCrypto.encrypt_data(encryption_key, bytes_data)
print('Encrypted data:', encryption_data)

# Decrypt the ciphertext
decryption_data = ValkyrieCrypto.decrypt_data(encryption_key, encryption_data)
print('Decrypted data:', decryption_data)
```

In this example, we demonstrate how to use the Crypto module to encrypt and decrypt data using `AES-GCM`. We also 
showcase the ability to generate an argon key using Argon2.

### Unit Tests

The ValkyrieCrypto module includes unit tests to ensure that the module is working as intended. To run the unit tests, 
run the following command in the root directory of the project:

```bash
python -m unittest unittests/test_crypto.py
```

### Supported Classes and Functions

- `ValkyrieCrypto`: A class to encrypt and decrypt data using AES-GCM, AES-CTR, and AES-CBC.
    - `encrypt_data(key: bytes, data: any, mode: int = AES_CTR) -> dict`: Encrypts data using the specified encryption mode.
    - `decrypt_data(key: bytes, data: dict, mode: int = AES_CTR) -> str | bytes`: Decrypts data using the specified encryption mode.
    - `generate_argon_key(secret: str, salt: str, key_length: int = 32, time_cost: int = 2, memory_cost: int = 100, parallelism: int = 8) -> bytes`: Generates a key using Argon2.

### Supported Encryption Modes

The following encryption modes are available:
- `AES-GCM`: Strong encryption with authentication, ensuring data integrity and confidentiality.
- `AES-CTR`: Fast encryption, allowing parallel processing, but does not provide built-in authentication.
- `AES-CBC`: Basic encryption, slower due to sequential processing and requires a padding scheme for irregular length data.
