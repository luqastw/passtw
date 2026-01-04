# 🔐 passtw

One-command-line password generator + encrypted local vault. Minimal, secure and easy-to-use CLI tool in Python.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge\&logo=python\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=for-the-badge)

---

## Table of Contents

* [Project Overview](#project-overview)
* [Features](#features)
* [Requirements & Dependencies](#requirements--dependencies)
* [Installation](#installation)
* [Usage / CLI Commands](#usage--cli-commands)
* [Configuration](#configuration)
* [Security & Vault](#security--vault)
* [Project Structure](#project-structure)
* [Tests & Quality](#tests--quality)
* [Contribution](#contribution)
* [License](#license)

---

## Project Overview

passtw is a secure, minimalistic, and configurable command-line tool for generating and storing passwords locally in an encrypted vault. Designed for developers and sysadmins, it runs seamlessly on Linux, macOS, and Windows.

---

## Features

* Generate secure random passwords;
* Encrypted local vault storage (AES-128);
* Configuration of password policies (character classes);
* Key generation and rotation;
* CLI-based usage with multiple commands;
* Cross-platform support (Linux / macOS / Windows);
* Clean project structure (`src/`, `tests/`);
* Automated tests for reliability.

---

## Requirements & Dependencies

* Python 3.10+;
* pip and pipx;
* Optional: virtual environment for isolation.

---

## Installation

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
./install.ps1
```

---

## Usage / CLI Commands

### Generate a new password

```bash
passtw gen {password name}
```

### Get a password from vault

```bash
passtw get {password name}
```

###### Include -c or --copy to copy to clipboard

### Remove a password from vault

```bash
passtw rm {password name}
```

### Lists all passwords in vault

```bash
passtw ls
```

### Set password policy options

```bash
passtw set {option}
```

### Unset password policy options

```bash
passtw unset {option}
```

### Generate a new cryptographic key

```bash
passtw keygen
```

### Show actual configuration

```bash
passtw conf
```

Use `passtw --help` for all available commands and options.

---

## Configuration

* Configuration is stored locally in JSON format.
* You can adjust password inclusion of symbols, numbers, and other parameters.
* `set` and `unset` commands allow dynamic updates without editing the config manually.

---

## Security & Vault

* Passwords are stored in an encrypted local vault using AES-128.
* Keys are generated and managed internally by the `keygen` module.
* No external storage or cloud dependencies — full local control.
* Recommended file permissions: restrict access to vault files to the current user only.

---

## Project Structure

```
src/
  ├── cli.py             # CLI entry point
  ├── generator.py       # Password generation logic
  ├── crypto_manager.py  # Encryption / decryption functions
  ├── config_loader.py   # Load / manage config
  ├── keygen.py          # Key generation / rotation
  ├── paths.py           # Paths and directories helper
  └── preferences.py     # Default preferences (immutable guide)
tests/                   # Automated test suite (pytest)
LICENSE
README.md
pyproject.toml / setup.py
requirements.txt
install.sh / install.ps1
```

---

## Tests & Quality

Run automated tests with:

```bash
make test
```

All critical modules including password generation, encryption/decryption, and configuration management are tested.

---

## Contribution

* Fork the repository;
* Create a feature branch (`git checkout -b feature/my-feature`);
* Commit your changes (`git commit -m 'Add new feature'`);
* Push to branch (`git push origin feature/my-feature`);
* Open a Pull Request.

Please follow the existing code style and write tests for new features.

---

## License

MIT License.
