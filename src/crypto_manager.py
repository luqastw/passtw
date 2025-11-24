from cryptography.fernet import Fernet
from src.paths import KEY_FILE, VAULT_FILE
from src.keygen import generate_key
import json

class CryptoManager():
    def _load_key(self):
        if KEY_FILE.exists(): 
            return KEY_FILE.read_bytes()
        else: 
            generate_key()
            return KEY_FILE.read_bytes()

    def _get_fernet(self):
        self.key = self._load_key()
        return Fernet(self.key)

    def _encrypt_password(self, password: str) -> bytes:
        self.f = self._get_fernet()
        return self.f.encrypt(password.encode())

    def _decrypt_password(self, crypt_password: bytes):
        self.f = self._get_fernet()
        return self.f.decrypt(crypt_password).decode()

    def _save_to_vault(self, name: str, encrypted: bytes):
        self.str_token = encrypted.decode()

        if VAULT_FILE.exists():
            self.data = json.loads(VAULT_FILE.read_text())
        else:
            self.data = {}

        self.data[name] = self.str_token
        VAULT_FILE.write_text(json.dumps(self.data, indent=4))

    def _read_from_vault(self, name: str) -> str:
        if not VAULT_FILE.exists():
            VAULT_FILE.write_text(json.dumps({}, indent=4))
            raise FileNotFoundError("Vault.json not found. Creating...")

        self.data = json.loads(VAULT_FILE.read_text())

        self.token_str = self.data.get(name)
        if self.token_str is None:
            raise ValueError("Password not found.")

        self.token_bytes = self.token_str.encode()
        return decrypt_password(self.token_bytes)

    def _password_encrypt(self, name, password):
        encrypted_password = self._encrypt_password(password)
        self._save_to_vault(name, encrypted_password)

    def crypt_password(self, name, password):
        return self._password_encrypt(name, password)

    def read_password(self, name):
        return self._read_from_vault(name)

    
def crypt_generated(name, password):
    manager = CryptoManager()
    manager.crypt_password(name, password)
