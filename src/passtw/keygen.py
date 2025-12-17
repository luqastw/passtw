from cryptography.fernet import Fernet
from passtw.paths import KEY_FILE
import os, stat

def secure_permissions(file):
    os.chmod(file, stat.S_IRUSR | stat.S_IWUSR)

def generate_key():
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    return secure_permissions(KEY_FILE)
