try:
    from cryptography.fernet import Fernet
    _HAS_CRYPTOGRAPHY = True
except ImportError:
    import base64
    _HAS_CRYPTOGRAPHY = False

class EncryptionModule:
    def __init__(self, key=None):
        """
        Initialize with an optional key. If no key is provided, generates a new one.
        In a real scenario, this key should be securely stored.
        """
        if _HAS_CRYPTOGRAPHY:
            if key:
                self.key = key
            else:
                self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)
        else:
            print("[WARNING] 'cryptography' module not found. Using simple Base64 mock encryption.")
            self.key = b'mock-key'

    def get_key(self):
        return self.key

    def encrypt(self, data):
        """
        Encrypts string or bytes data. Returns bytes.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if _HAS_CRYPTOGRAPHY:
            return self.cipher.encrypt(data)
        else:
            # Mock encryption: Base64 encode
            return base64.b64encode(data)

    def decrypt(self, encrypted_data):
        """
        Decrypts bytes data. Returns string.
        """
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode('utf-8')
            
        if _HAS_CRYPTOGRAPHY:
            return self.cipher.decrypt(encrypted_data).decode('utf-8')
        else:
            # Mock decryption: Base64 decode
            try:
                return base64.b64decode(encrypted_data).decode('utf-8')
            except:
                return str(encrypted_data)

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
