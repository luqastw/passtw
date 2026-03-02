# passtw

A command-line password manager that generates cryptographically secure passwords and stores them in an encrypted local vault. Built with Python, designed for developers and system administrators who prefer offline, terminal-native tooling.

![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![CI](https://github.com/luqastw/passtw/actions/workflows/ci.yml/badge.svg)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Security Model](#security-model)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

passtw is a single-binary CLI tool that combines password generation with encrypted local storage. It requires no external services, no cloud accounts, and no background processes. All data stays on disk, encrypted at rest.

**Key characteristics:**

- Cryptographically secure password generation using Python's `secrets` module
- AES-128-CBC encryption with HMAC-SHA256 integrity verification (Fernet)
- Cross-platform data storage following OS conventions (XDG on Linux, `~/Library` on macOS, `%APPDATA%` on Windows)
- Zero network dependencies -- fully offline operation

---

## Architecture

```
src/passtw/
  cli.py              CLI entry point and command routing (Click)
  generator.py        Password generation engine
  crypto_manager.py   Fernet-based encryption and vault I/O
  config_loader.py    JSON configuration persistence
  keygen.py           Cryptographic key generation with file permission enforcement
  paths.py            Platform-aware data directory resolution
  preferences.py      Password policy dataclass
```

The project follows a layered design where each module encapsulates a single responsibility:

| Layer | Module | Responsibility |
|-------|--------|----------------|
| Interface | `cli.py` | Parses commands, orchestrates workflows, handles user interaction |
| Generation | `generator.py` | Builds character pools, applies Fisher-Yates shuffle via `secrets.randbelow()` |
| Storage | `crypto_manager.py` | Encrypts passwords with Fernet, reads/writes `vault.json` |
| Configuration | `config_loader.py` | Manages `config.json`, validates policy constraints |
| Infrastructure | `paths.py`, `keygen.py` | Resolves OS-specific paths via `platformdirs`, generates keys with restricted permissions |

### Data Flow

```
User command --> cli.py --> generator.py (generate password)
                       --> crypto_manager.py (encrypt + store)
                       --> config_loader.py (read policy)
                       --> paths.py (resolve file locations)
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `cryptography` | Fernet symmetric encryption (AES-128-CBC + HMAC-SHA256) |
| `click` | Command-line interface framework |
| `platformdirs` | OS-native data directory resolution |
| `pyperclip` | Clipboard integration for password retrieval |
| `pygments` | Syntax-highlighted output |

---

## Security Model

### Password Generation

Passwords are generated using `secrets.SystemRandom`, which draws from the operating system's cryptographic random number generator (`/dev/urandom` on Linux, `CryptGenRandom` on Windows). The generation process:

1. Builds a character pool from the active policy (uppercase, lowercase, digits, symbols)
2. Guarantees at least one character from each enabled category
3. Fills remaining positions with uniformly random selections from the full pool
4. Applies a Fisher-Yates shuffle using `secrets.randbelow()` to eliminate positional bias

### Encryption

Passwords are encrypted using **Fernet**, which provides authenticated encryption:

- **Cipher:** AES-128 in CBC mode
- **Integrity:** HMAC-SHA256
- **Key derivation:** Fernet key generated via `Fernet.generate_key()` (128-bit, URL-safe base64 encoded)
- **Storage:** Encrypted tokens stored as base64 strings in `vault.json`

### File Permissions

The encryption key file (`secret.key`) is created with `0600` permissions (owner read/write only), enforced programmatically via `os.chmod()` using `stat.S_IRUSR | stat.S_IWUSR`.

### Threat Model

passtw is designed for local, single-user password management. It protects against:

- Plaintext password exposure on disk
- Unauthorized file access (via OS-level permissions)
- Tampered ciphertext (via HMAC verification)

It does not protect against:

- Keyloggers or memory-scraping malware on a compromised host
- Attackers with root/admin access to the machine

---

## Installation

**Prerequisites:** Python 3.10+ and [pipx](https://pypa.github.io/pipx/).

### Linux / macOS

```bash
git clone https://github.com/luqastw/passtw.git
cd passtw
sh install.sh
```

### Windows (PowerShell)

```powershell
git clone https://github.com/luqastw/passtw.git
cd passtw
.\install.ps1
```

### Manual Installation

```bash
pipx install .
passtw init
```

After installation, run `passtw init` to generate the encryption key and create the vault.

---

## Usage

```bash
passtw gen <name>           # Generate a new password and store it
passtw get <name>           # Retrieve a password from the vault
passtw get <name> -c        # Retrieve and copy to clipboard
passtw ls                   # List all stored password entries
passtw rm <name>            # Remove a password (with confirmation)
passtw set <option>         # Enable a character type in the policy
passtw unset <option>       # Disable a character type in the policy
passtw conf                 # Display current configuration
passtw keygen               # Generate a new encryption key
passtw --help               # Show all commands and options
```

### Examples

```bash
# Generate a password for a GitHub account
passtw gen github

# Copy the password to clipboard
passtw get github -c

# Disable symbols in generated passwords
passtw unset sims

# Check current policy
passtw conf
```

---

## Configuration

Configuration is stored in `config.json` within the platform-specific data directory:

| OS | Path |
|----|------|
| Linux | `~/.local/share/passtw/config.json` |
| macOS | `~/Library/Application Support/passtw/config.json` |
| Windows | `%APPDATA%\passtw\config.json` |

The policy controls which character classes are included in generated passwords:

| Option | Description | Default |
|--------|-------------|---------|
| `upper` | Uppercase letters (A-Z) | Enabled |
| `lower` | Lowercase letters (a-z) | Enabled |
| `nums` | Digits (0-9) | Enabled |
| `sims` | Symbols (!@#$%...) | Enabled |

At least one character class must remain enabled at all times.

For development, set `PASSTW_ENV=dev` to use a local `./data` directory instead of the system path.

---

## Development

The project uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

```bash
# Install dependencies
make install

# Run in development mode
make run ARGS='init'
make run ARGS='gen test'

# Build the package
make build

# Clean build artifacts
make clean
```

### Dev Dependencies

| Tool | Purpose |
|------|---------|
| `pytest` | Test runner |
| `ruff` | Linter |
| `black` | Code formatter |
| `bandit` | Security static analysis (SAST) |
| `pip-audit` | Dependency vulnerability scanning |
| `pyfakefs` | Filesystem isolation for tests |

---

## Testing

```bash
make test       # Run unit tests
make sec        # Run security checks (Bandit + pip-audit)
```

The test suite covers the three core modules:

| Module | Tests | Coverage |
|--------|-------|----------|
| `generator.py` | Password structure, character pool constraints, shuffle correctness, factory wrappers | 7 tests |
| `crypto_manager.py` | Encrypt/decrypt roundtrip, duplicate detection, missing key/vault errors | 8 tests |
| `config_loader.py` | Default creation, config loading, validation constraints, directory setup | 4 tests |

Tests use `pyfakefs` for filesystem isolation, ensuring no test touches the real filesystem. Mock objects are used to inject dependencies and verify behavior without side effects.

### CI/CD

A GitHub Actions pipeline runs on every push and pull request to `main` and `develop`:

1. Install dependencies via Poetry
2. Initialize the application
3. Run the full test suite
4. Run security scans (Bandit for SAST, pip-audit for dependency vulnerabilities, Safety for known CVEs)

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Write tests for new functionality
4. Ensure all checks pass (`make test && make sec`)
5. Submit a pull request

Please follow the existing code style. The project uses `black` for formatting and `ruff` for linting.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
