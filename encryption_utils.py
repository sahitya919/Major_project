from cryptography.fernet import Fernet
import base64
import os

class EncryptionModule:
    def __init__(self, key=None):
        """
        Initialize with an optional key. If no key is provided, generates a new one.
        In a real scenario, this key should be securely stored.
        """
        if key:
            self.key = key
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def get_key(self):
        return self.key

    def encrypt(self, data):
        """
        Encrypts string or bytes data. Returns bytes.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.cipher.encrypt(data)

    def decrypt(self, encrypted_data):
        """
        Decrypts bytes data. Returns string.
        """
        if isinstance(encrypted_data, str):
            # If passed as string representation of bytes, ensure it's bytes
            encrypted_data = encrypted_data.encode('utf-8')
        return self.cipher.decrypt(encrypted_data).decode('utf-8')

    def try_decrypt(self, data):
        """
        Attempts to decrypt data. If successful, returns decrypted string.
        If fails (invalid token, not encrypted), returns original data (as string).
        Used for mixed input handling.
        """
        try:
            return self.decrypt(data)
        except Exception:
            # Fallback for plaintext input
            if isinstance(data, bytes):
                return data.decode('utf-8', errors='ignore')
            return str(data)
