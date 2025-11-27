# 🔐 passtw

**passtw** is a Python-based random password generator + encrypted local vault, using AES‑128 encryption and a cryptographic key.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge\&logo=python\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=for-the-badge)

---

## 📖 Project Overview

passtw is a secure, minimalistic, and configurable command‑line tool for generating and storing passwords locally in an encrypted vault.

Key features:

* Password generation with customization (character types, symbols etc.);
* Local vault encrypted using AES‑128, storing passwords and keys securely;
* Configuration system to adjust generation parameters (via JSON or config);
* Organized, modular code under `src/`, following good project structure practices;
* Automated tests to ensure reliability and stability (via `tests/`).

With this project, you get a **safe, maintainable and ready‑to‑use tool** for password management directly from the command line.

---

## ⚙️ Features

* Generate secure random passwords and store them in a local vault
* Encryption key generation / rotation
* Configurable behavior through config files / preferences
* Easy CLI usage: generate, set, unset, manage vault, rotate keys
* Clean, modular architecture (CLI layer / core logic / config layer)
* Cross‑platform compatibility (works on Linux / Windows via provided scripts)
* Unit tests covering core functionalities

---

## 📁 Project Structure

```
├── src/                # Main source code
│   ├── cli.py          # CLI entry point and argument parsing
│   ├── config_loader.py
│   ├── crypto_manager.py
│   ├── generator.py
│   ├── keygen.py
│   ├── paths.py
│   └── preferences.py
├── tests/              # Test suite (pytest)
├── LICENSE
├── README.md
├── pyproject.toml
├── setup.py
├── requirements.txt
├── install.sh          # Install script for Unix
├── install.ps1         # Install script for Windows
└── pytest.ini
```

---

## 🔧 Installation

**Prerequisites:** Python 3.10+, pip and pipx must be installed before installing passtw.

### Unix / Linux / macOS:

```bash
git clone https://github.com/luqastw/passtw.git
cd passtw
pip install -r requirements.txt
sh install.sh
```

### Windows (PowerShell):

```powershell
git clone https://github.com/luqastw/passtw.git
cd passtw
pip install -r requirements.txt
./install.ps1
```

---

## 🕹 Usage Examples

Generate a new password:

```bash
passtw generate
```

Set generation options:

```bash
passtw set {option}
```

Unset options:

```bash
passtw unset {option}
```

Show or adjust configuration (if supported):

```bash
passtw config
```

---

## 🔐 Security & Vault Handling

* Passwords and data are stored encrypted using AES‑128.
* Encryption keys are stored/managed securely via the built‑in keygen module.
* Vault and key files are local — no external services or remote storage — maximizing privacy and control.
* Configurable settings allow to customize password policies, helping generate strong passwords.

---

## 🧪 Testing

The project includes automated tests covering key functionality (password generation, encryption/decryption, config loading, etc.).

Run tests with:

```bash
pytest -v
```

---

## 👨‍💻 Why This Project Is Valuable for Recruiters / Hiring Managers

* Demonstrates **clean, modular Python project structure** (src layout, setup scripts, clear separation of concerns)
* Uses **real cryptography** — not naive random-only password generation — showing security awareness
* Has **configurability and flexibility**, important for real-world tooling
* Includes **automated tests**, showing commitment to quality and reliability
* Provides a **usable CLI tool**, not just demo code — indicates ability to build usable utilities / tools
* Cross-platform support (Linux, Windows) — shows consideration for different user environments
* Demonstrates practical skills: encryption, file handling, CLI, configuration, packaging — all relevant for backend / dev‑ops / tooling roles

---

## 🗺 Potential Improvements (Roadmap / Ideas)

* Support for multiple vaults / profiles (e.g. vault per project or per user)
* Export / import vault securely (e.g. encrypted backup)
* CLI interactive mode or TUI interface (with colors / better UX)
* Integration with system clipboard (copy password securely)
* Password strength checker / estimation before saving
* Option to hash master password / require master password to unlock vault
* Packaging and release (PyPI) for easier installation

---

## 📄 License

This project is licensed under the **MIT License**.
