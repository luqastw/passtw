from cryptography.fernet import Fernet
from src.paths import KEY_FILE, VAULT_FILE
import json

def load_key():
    return KEY_FILE.read_bytes()

def get_fernet():
    key = load_key()
    return Fernet(key)

def encrypt_password(password: str) -> bytes:
    f = get_fernet()
    return f.encrypt(password.encode())

def decrypt_password(crypt_password: bytes):
    f = get_fernet()
    return f.decrypt(crypt_password).decode()

def save_to_vault(name: str, encrypted: bytes):
    str_token = encrypted.decode()

    if VAULT_FILE.exists():
        data = json.loads(VAULT_FILE.read_text())
    else:
        data = {}

    data[name] = str_token
    VAULT_FILE.write_text(json.dumps(data, indent=4))

def read_from_vault(name: str) -> str:
    if not VAULT_FILE.exists():
        VAULT_FILE.write_text(json.dumps({}, indent=4))
        raise FileNotFoundError("Vault.json not found. Creating...")

    data = json.loads(VAULT_FILE.read_text())

    token_str = data.get(name)
    if token_str is None:
        raise ValueError("Password not found.")

    token_bytes = token_str.encode()
    return decrypt_password(token_bytes)