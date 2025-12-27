import json
import pytest
import click
from pathlib import Path
from unittest.mock import patch
from cryptography.fernet import Fernet
from passtw.crypto_manager import CryptoManager, crypt_generated

FAKE_KEY_PATH = Path("/fake/path/secret.key")
FAKE_VAULT_PATH = Path("/fake/path/vault.json")
VALID_KEY = Fernet.generate_key()

@pytest.fixture
def mock_paths(fs):
    fs.create_dir(FAKE_KEY_PATH.parent)
    with patch("passtw.crypto_manager.KEY_FILE", FAKE_KEY_PATH), \
         patch("passtw.crypto_manager.VAULT_FILE", FAKE_VAULT_PATH):
        yield

class TestCryptoManager:

    def test_init_raises_error_no_key(self, fs, mock_paths):
        assert not FAKE_KEY_PATH.exists()

        with pytest.raises(click.ClickException) as excinfo:
            CryptoManager()

        assert "Key not found" in str(excinfo.value)

    def test_encrypt_and_save_success(self, fs, mock_paths):
        fs.create_file(FAKE_KEY_PATH, contents=VALID_KEY)

        manager = CryptoManager()
        manager.crypt_password("facebook", "minha_senha_123")

        assert FAKE_VAULT_PATH.exists()
        vault_content = json.loads(FAKE_VAULT_PATH.read_text())

        assert "facebook" in vault_content

        f = Fernet(VALID_KEY)
        decrypted = f.decrypt(vault_content["facebook"].encode()).decode()
        assert decrypted == "minha_senha_123"

    def test_save_raises_error_duplicate(self, fs, mock_paths):
        fs.create_file(FAKE_KEY_PATH, contents=VALID_KEY)

        manager = CryptoManager()
        manager.crypt_password("github", "123")

        with pytest.raises(click.ClickException) as excinfo:
            manager.crypt_password("github", "456")

        assert "already exists" in str(excinfo.value)

    def test_read_password_success(self, fs, mock_paths):
        f = Fernet(VALID_KEY)
        token = f.encrypt(b"segredo_maximo").decode()
        vault_data = {"amazon": token}

        fs.create_file(FAKE_KEY_PATH, contents=VALID_KEY)
        fs.create_file(FAKE_VAULT_PATH, contents=json.dumps(vault_data))

        manager = CryptoManager()
        resultado = manager.read_password("amazon")

        assert resultado == "segredo_maximo"

    def test_read_raises_error_password_not_found(self, fs, mock_paths):
        fs.create_file(FAKE_KEY_PATH, contents=VALID_KEY)
        fs.create_file(FAKE_VAULT_PATH, contents=json.dumps({}))

        manager = CryptoManager()

        with pytest.raises(click.ClickException) as excinfo:
            manager.read_password("twitter")

        assert "Password not found" in str(excinfo.value)

    def test_read_raises_error_vault_missing(self, fs, mock_paths):
        fs.create_file(FAKE_KEY_PATH, contents=VALID_KEY)

        manager = CryptoManager()

        with pytest.raises(click.ClickException) as excinfo:
            manager.read_password("google")

        assert "Vault.json not found" in str(excinfo.value)
        assert FAKE_VAULT_PATH.exists()

def test_standalone_crypt_generated(fs, mock_paths):
    fs.create_file(FAKE_KEY_PATH, contents=VALID_KEY)

    crypt_generated("linkedin", "senha_gerada")

    vault_content = json.loads(FAKE_VAULT_PATH.read_text())
    assert "linkedin" in vault_content
