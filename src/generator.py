from src.paths import CONFIG_FILE
from src.preferences import Preferences
from src.config_loader import read_preferences
from typing import Dict
import secrets, string, random

PASSWORD = []
CHAR_POOL = {}

BASE_POOL = {
    "upper": string.ascii_uppercase,
    "lower": string.ascii_lowercase,
    "nums": string.digits,
    "sims": string.punctuation
}

def build_pool():
    data = read_preferences()

    if data.upper is True: CHAR_POOL["upper"] = BASE_POOL["upper"]
    if data.lower is True: CHAR_POOL["lower"] = BASE_POOL["lower"]
    if data.nums is True: CHAR_POOL["nums"] = BASE_POOL["nums"]
    if data.sims is True: CHAR_POOL["sims"] = BASE_POOL["sims"]
    return CHAR_POOL

def pick_chars():
    for i in CHAR_POOL.values():
        PASSWORD.append(secrets.choice(i))
    return PASSWORD

def fill_with_random():
    ALL_CHARS = "".join(CHAR_POOL.values())
    remaining = 16 - len(PASSWORD)

    for _ in range(remaining):
        PASSWORD.append(secrets.choice(ALL_CHARS))

    print(PASSWORD)

def secure_shuffle(seq):
    seq = list(seq)

    for i in range(len(seq) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        seq[i], seq[j] = seq[j], seq[i]

    return seq
    
build_pool()
pick_chars()
fill_with_random()
PASSWORD = secure_shuffle(PASSWORD)
finalpass = ''.join(PASSWORD)
print(finalpass)