# AES-256 Encryption Utilities
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from ..config import settings

def _get_key():
    """Generate or retrieve encryption key"""
    if settings.ENCRYPTION_KEY:
        # Use provided key
        key = settings.ENCRYPTION_KEY.encode()
    else:
        # Generate key from secret (for development)
        salt = b'sme_financial_health_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode()))
    return key

_fernet = None

def _get_fernet():
    global _fernet
    if _fernet is None:
        _fernet = Fernet(_get_key())
    return _fernet

def encrypt_data(data: str) -> str:
    """Encrypt sensitive data using AES-256 (Fernet)"""
    if not data:
        return data
    fernet = _get_fernet()
    encrypted = fernet.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt data encrypted with AES-256"""
    if not encrypted_data:
        return encrypted_data
    fernet = _get_fernet()
    decoded = base64.urlsafe_b64decode(encrypted_data.encode())
    decrypted = fernet.decrypt(decoded)
    return decrypted.decode()

def generate_encryption_key() -> str:
    """Generate a new encryption key (use for setup)"""
    return Fernet.generate_key().decode()
