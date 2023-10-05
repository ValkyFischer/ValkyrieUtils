## Valkyrie Compressor Module

The Compressor module (`Compressor.py`) provides a utility to compress and decompress data using various compression modes such as gzip, bzip2, lzma, lz4, zstd, and none (no compression). It offers functions to compress and decompress data based on the specified compression mode.

### Usage

1. Import the Compressor module into your Python script.
2. Use the `ValkyrieCompressor` class to compress and decompress data with various compression modes.
3. Choose a compression mode and call the respective functions to compress and decompress data.

### Example

```python
from Compressor import ValkyrieCompressor
# Run a test
sample_data = b"Sample data to be compressed"
sample_compressed = ValkyrieCompressor.deflate(sample_data, 'zstd')
sample_decompressed = ValkyrieCompressor.inflate(sample_compressed, 'zstd')

# Print the results
print(f"Original data     : {sample_data}")
print(f"Compressed data   : {sample_compressed}")
print(f"Decompressed data : {sample_decompressed}")
```

In this example, we demonstrate how to use the Compressor module to compress and decompress data using `Zstandard` compression.


### Unit Tests

The ValkyrieCompressor module includes unit tests to ensure that the module is working as intended. To run the unit tests, 
run the following command in the root directory of the project:

```bash
python -m unittest unittests/test_compressor.py
```

### Supported Classes and Functions

- `ValkyrieCompressor`: A class to compress and decompress data using various compression modes such as gzip, bzip2, lzma, lz4, zstd, and none.
    - `deflate(raw_data, compression_mode='zstd')`: Compress the given data using the specified compression mode.
    - `inflate(compressed_data, compression_mode='zstd')`: Decompress the given compressed data using the specified compression mode.

### Supported Compression Modes

The following compression modes are available:
- `Gzip (Balanced)`: Provides a balance between compression speed and file size reduction.
- `ZSTD (Balanced)`: Uses Zstandard compression, which offers a good trade-off between speed and compression ratio.
- `Bzip2 (Slow)`: Offers a high compression ratio but is relatively slow in comparison to other methods.
- `LZMA (Slow)`: Provides excellent compression at the cost of slower compression and decompression speeds.
- `LZ4 (Fast)`: Prioritizes speed over compression ratio, making it ideal for scenarios where fast decompression is crucial.
