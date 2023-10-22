

class EncryptionError(Exception):
    """Exception raised for errors related to encryption in VPK packages."""

    def __init__(self, message="The VPK package is not correctly encrypted."):
        self.message = message
        super().__init__(self.message)


class DecryptionError(Exception):
    """Exception raised for errors related to decryption in VPK packages."""

    def __init__(self, message="The VPK package is not correctly decrypted."):
        self.message = message
        super().__init__(self.message)


class CompressorError(Exception):
    """Exception raised for errors related to compression in VPK packages."""

    def __init__(self, message="The VPK package is not correctly compressed."):
        self.message = message
        super().__init__(self.message)


class VersionError(Exception):
    """Exception raised for errors related to the version of VPK packages."""

    def __init__(self, message="The VPK package is not compatible with this version of Valkyrie Utils."):
        self.message = message
        super().__init__(self.message)

class VpkError(Exception):
    """Exception raised for errors related to VPK packages."""

    def __init__(self, message="An error occurred while processing the VPK package."):
        self.message = message
        super().__init__(self.message)

class ConfigError(Exception):
    """Exception raised for errors related to configuration files."""

    def __init__(self, message="An error occurred while processing the configuration file."):
        self.message = message
        super().__init__(self.message)
