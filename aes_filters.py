from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os

class AESPlugin:
    def __init__(self):
        self.salt = b'static_salt_value'  # Change this to a securely stored salt

    def derive_key(self, password: str) -> bytes:
        """Derives a 32-byte key from the given password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    def encrypt(self, plaintext: str, password: str) -> str:
        """Encrypts a plaintext string using AES."""
        key = self.derive_key(password)
        iv = os.urandom(16)  # Generate a new IV for each encryption
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        # Pad plaintext to be a multiple of 16 bytes
        padded_plaintext = plaintext + (16 - len(plaintext) % 16) * chr(16 - len(plaintext) % 16)
        ciphertext = encryptor.update(padded_plaintext.encode()) + encryptor.finalize()

        return base64.b64encode(iv + ciphertext).decode()

    def decrypt(self, encrypted_text: str, password: str) -> str:
        """Decrypts an AES-encrypted string."""
        key = self.derive_key(password)
        data = base64.b64decode(encrypted_text)

        iv, ciphertext = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_padded[:-decrypted_padded[-1]].decode()  # Remove padding

    def filters(self):
        """Return the available filters."""
        return {
            "aes_encrypt": self.encrypt,
            "aes_decrypt": self.decrypt,
        }

# Ansible expects a function that returns the filter dictionary
def aes_filters():
    return AESPlugin().filters()