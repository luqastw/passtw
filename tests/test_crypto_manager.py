from passtw.crypto_manager import CryptoManager
from passtw.generator import PasswordGenerator
from passtw.paths import VAULT_FILE
import random, json

generator = PasswordGenerator()
random_password = generator.generate()
vault_data = json.loads(VAULT_FILE.read_text())

def test_load_vault():
    if not VAULT_FILE.exists():
        pytest.skip("Skipping test: Vault file don't exist in this enviroment (CI)")

def test_load_key():
    manager = CryptoManager()
    test_load_vault()
    manager._load_key()
    
def test_get_fernet():  
    manager = CryptoManager()
    test_load_vault()
    manager._get_fernet()

def test_encrypt_password():
    manager = CryptoManager()
    test_load_vault()
    manager._encrypt_password(random_password)