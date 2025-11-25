from src.crypto_manager import CryptoManager

def test_load_key():
    manager = CryptoManager()
    manager._load_key()
    
def test_get_fernet():  
    manager = CryptoManager()
    manager._get_fernet()

def test_encrypt_password():
    manager = CryptoManager()
    manager._encrypt_password()