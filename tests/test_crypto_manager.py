from passtw.crypto_manager import CryptoManager
from passtw.generator import PasswordGenerator
from passtw.paths import VAULT_FILE
import random, json

generator = PasswordGenerator()
random_password = generator.generate()
vault_data = json.loads(VAULT_FILE.read_text())

def test_load_key():
    manager = CryptoManager()
    manager._load_key()
    
def test_get_fernet():  
    manager = CryptoManager()
    manager._get_fernet()

def test_encrypt_password():
    manager = CryptoManager()
    manager._encrypt_password(random_password)

def test_decrypt_password():
    manager = CryptoManager()