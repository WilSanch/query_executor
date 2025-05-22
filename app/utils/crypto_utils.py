from cryptography.fernet import Fernet
import os

FERNET_KEY = os.environ.get("FERNET_KEY", Fernet.generate_key())
fernet = Fernet(FERNET_KEY)

def encrypt_string(s: str) -> str:
    return fernet.encrypt(s.encode()).decode()

def decrypt_string(s: str) -> str:
    return fernet.decrypt(s.encode()).decode()