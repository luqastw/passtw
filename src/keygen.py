from cryptography.fernet import Fernet
from src.paths import KEY_FILE
from pathlib import Path

def generate_key():
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)