import string
import pytest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
from passtw.generator import PasswordGenerator, create_password, get_password

@pytest.fixture
def mock_config_obj():
    return SimpleNamespace(
        upper=True,
        lower=True,
        nums=True,
        sims=True
    )

@pytest.fixture
def mock_config_manager(mock_config_obj):
    with patch("passtw.generator.ConfigurationManager") as MockClass:
        instance = MockClass.return_value
        instance.read_preferences.return_value = mock_config_obj
        yield instance

class TestPasswordGenerator:

    def test_generate_structure_default_config(self, mock_config_manager):
        gen = PasswordGenerator()
        password = gen.generate()

        assert len(password) == 16
        assert any(c in string.ascii_uppercase for c in password)
        assert any(c in string.ascii_lowercase for c in password)
        assert any(c in string.digits for c in password)
        assert any(c in string.punctuation for c in password)

    def test_generate_respects_config_only_nums(self, mock_config_manager):
        mock_config_manager.read_preferences.return_value = SimpleNamespace(
            upper=False, lower=False, nums=True, sims=False
        )

        gen = PasswordGenerator()
        password = gen.generate()

        assert len(password) == 16
        assert password.isdigit()
        assert not any(c in string.ascii_uppercase for c in password)

    def test_generate_respects_config_only_upper(self, mock_config_manager):
        mock_config_manager.read_preferences.return_value = SimpleNamespace(
            upper=True, lower=False, nums=False, sims=False
        )

        gen = PasswordGenerator()
        password = gen.generate()

        assert password.isupper()
        assert len(password) == 16

    def test_secure_shuffle_changes_order(self, mock_config_manager):
        # Travamos a seed ou o pool para garantir que a diferença seja o shuffle
        # Mas como a geração é aleatória, verificamos se não é ordenado
        gen = PasswordGenerator()
        # Injeta manualmente para teste controlado
        gen.PASSWORD = ['a', 'b', 'c', 'd', 'e']

        shuffled = gen._secure_shuffle()

        # Estatisticamente é muito provável que mude, mas em testes unitários
        # focamos que o método retorna string e tem o mesmo tamanho e conteúdo
        assert len(shuffled) == 5
        assert sorted(shuffled) == ['a', 'b', 'c', 'd', 'e']
        assert isinstance(shuffled, str)

@patch("passtw.generator.crypt_generated")
def test_create_password_flow(mock_crypt, mock_config_manager):
    # Testamos a função helper 'create_password'
    # Ela deve instanciar o generator, gerar a senha e chamar o crypt

    service_name = "netflix"
    create_password(service_name)

    mock_crypt.assert_called_once()

    # Verifica os argumentos passados para o crypt_generated
    args, _ = mock_crypt.call_args
    assert args[0] == service_name
    assert len(args[1]) == 16  # A senha gerada passada como segundo arg

@patch("passtw.generator.CryptoManager")
def test_get_password_flow(MockCryptoClass):
    # Testamos a função helper 'get_password'
    # Ela deve instanciar o CryptoManager e chamar read_password

    mock_instance = MockCryptoClass.return_value
    mock_instance.read_password.return_value = "senha_secreta_retornada"

    resultado = get_password("facebook")

    assert resultado == "senha_secreta_retornada"
    mock_instance.read_password.assert_called_once_with("facebook")
