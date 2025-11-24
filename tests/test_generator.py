from src.generator import create_password, get_password
from src.paths import VAULT_FILE
import secrets, random, string, json

def generate_name():
    chars = string.ascii_letters
    name = ''
    for _ in range(10):
        name += "".join(secrets.choice(chars))
    return name

def get_random_password():
    data = json.loads(VAULT_FILE.read_text())
    key = random.choice(list(data.keys()))
    return key

def test_create_password():
    create_password(generate_name())

def test_get_password():
    get_password(get_random_password())