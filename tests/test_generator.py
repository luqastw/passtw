from passtw.generator import create_password, get_password
from passtw.paths import VAULT_FILE
import secrets
import random
import string
import json
import pytest

@pytest.mark.skip(reason='Refactor needed using mocker. Release v1.1.0')
def generate_name():
    chars = string.ascii_letters
    name = ''
    for _ in range(10):
        name += "".join(secrets.choice(chars))
    return name

@pytest.mark.skip(reason='Refactor needed using mocker. Release v1.1.0')
def get_random_password():
    data = json.loads(VAULT_FILE.read_text())
    key = random.choice(list(data.keys()))
    return key

@pytest.mark.skip(reason='Refactor needed using mocker. Release v1.1.0')
def test_create_password():
    create_password(generate_name())

@pytest.mark.skip(reason='Refactor needed using mocker. Release v1.1.0')
def test_get_password():
    get_password(get_random_password())
