from passtw.config_loader import ConfigurationManager
from passtw.crypto_manager import crypt_generated, CryptoManager
from passtw.preferences import Preferences
import string, secrets

class PasswordGenerator():
    def __init__(self):
        self.config = self._load_config()
        self.PASSWORD = []
        self.CHAR_POOL = {}
        self.ALL_CHARS = ''

    def _load_config(self):
        manager = ConfigurationManager()
        config = manager.read_preferences()
        return config

    def _build_pool(self):
        self.CHAR_POOL = {}

        if self.config.upper:
            self.CHAR_POOL["upper"] = string.ascii_uppercase
        if self.config.lower:
            self.CHAR_POOL["lower"] = string.ascii_lowercase
        if self.config.nums:
            self.CHAR_POOL["nums"] = string.digits
        if self.config.sims:
            self.CHAR_POOL["sims"] = string.punctuation

        return self.CHAR_POOL

    def _pick_chars(self):
        for chars in self.CHAR_POOL.values():
            self.PASSWORD.append(secrets.choice(chars))
        secrets.SystemRandom().shuffle(self.PASSWORD)

    def _fill_random(self):
        self.ALL_CHARS = "".join(self.CHAR_POOL.values())
        remaining = 16 - len(self.PASSWORD)

        for _ in range(remaining):
            self.PASSWORD.append(secrets.choice(self.ALL_CHARS))

    def _secure_shuffle(self):
        for i in range(len(self.PASSWORD) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            self.PASSWORD[i], self.PASSWORD[j] = self.PASSWORD[j], self.PASSWORD[i]

        return ''.join(self.PASSWORD)

    def generate(self):
        self._build_pool()
        self._pick_chars()
        self._fill_random()
        return self._secure_shuffle()

def create_password(name: str):
    generator = PasswordGenerator()
    generated_password = generator.generate()
    return crypt_generated(name, generated_password)

def get_password(name: str):
    manager = CryptoManager()
    return manager.read_password(name)
