import json import pytest
from unittest.mock import patch, MagicMock
from cryptography.fernet import Fernet
from click import ClickException
from passtw.crypto_manager import CryptoManager

FAKE_KEY = Fernet.generate_key()
f = Fernet(FAKE_KEY)
TEST_TOKEN = f.encrypt(b"test123").decode()
FAKE_VAULT = {"github": TEST_TOKEN}


@patch("pathlib.Path.read_bytes")
@patch("pathlib.Path.exists")
def test_init_raises_no_key(mock_exists, mock_read_bytes):
    mock_exists.return_value = False

    with pytest.raises(ClickException) as excinfo:
        CryptoManager()

    assert "Key not found" in str(excinfo.value)

    @patch("pathlib.Path.write_text")
    @patch("pathlib.Path.read_text")
    @patch("pathlib.Path.read_bytes")
    @patch("pathlib.Path.exists", return_value=True)
    def test_save_duplicate_error(
        mock_write_text, mock_read_text, mock_read_bytes, mock_exists
    ):
        mock_read_bytes.return_value = FAKE_KEY
        mock_read_text.return_value = json.dumps(FAKE_VAULT)
        manager = CryptoManager()

        with pytest.raises(ClickException) as excinfo:
            manager._save_to_vault("facebook", b"senha_nova_qualquer")
        assert "already exists" in str(excinfo.value)
        mock_write_text.assert_not_called()


@patch("pathlib.Path.read_text")
@patch("pathlib.Path.read_bytes")
@patch("pathlib.Path.exists", return_value=True)
def test_read_success(mock_exists, mock_bytes, mock_text):
    mock_bytes.return_value = FAKE_KEY
    mock_text.return_value = json.dumps(FAKE_VAULT)
    manager = CryptoManager()

    resultado = manager._read_from_vault("github")
    assert resultado == "test123"


@patch("pathlib.Path.read_bytes")
@patch("pathlib.Path.exists")
@patch('pathlib.Path.read_text')
def test_load_key(mock_read_text, mock_exists, mock_read_bytes):
    mock_read_text.return_value = json.dumps({})
    mock_exists.return_value = True
    mock_read_bytes.return_value = FAKE_KEY
    manager = CryptoManager()
    assert manager.key == FAKE_KEY


@patch("pathlib.Path.read_bytes")
@patch("pathlib.Path.read_text")
@patch("pathlib.Path.exists", return_value=True)
def test_load_vault(mock_read_bytes, mock_read_text, mock_exists):
    mock_read_bytes.return_value = FAKE_KEY
    mock_read_text.return_value = json.dumps(FAKE_VAULT)
    manager = CryptoManager()
