"""
Encryption Service - AES-256 encryption for financial data at rest
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Generate a key from secret (in production, use proper key management)
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
SALT = b"financial_health_salt"

def _get_fernet() -> Fernet:
    """Get Fernet instance with derived key"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(SECRET_KEY.encode()))
    return Fernet(key)

def encrypt_data(data: str) -> bytes:
    """Encrypt string data using AES-256 (Fernet)"""
    f = _get_fernet()
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypt data back to string"""
    f = _get_fernet()
    return f.decrypt(encrypted_data).decode()
