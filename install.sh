#!/bin/bash

R="\033[0;31m"
G="\033[0;32m"
Y="\033[1;33m"
C="\033[0;36m"
N="\033[0m"

LOG_FILE="install_debug.log"

detect_system() {
  local os="$(uname -s)"
  case "$os" in
  Linux) echo "Linux" ;;
  Darwin) echo "MacOS" ;;
  *) echo "Windows" ;;
  esac
}

loader() {
  local msg="$1"
  local pid=$!
  local delay=0.1
  local spinstr='|/-\'

  tput civis

  while ps -p $pid >/dev/null; do
    local temp=${spinstr#?}
    printf " [%c]  %s" "$spinstr" "$msg"
    local spinstr=$temp${spinstr%"$temp"}
    sleep $delay
    printf "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
  done

  tput cnorm
  printf "                                                          \r"
}

run_safe() {
  "$@" >>"$LOG_FILE" 2>&1
  return $?
}

rm -f "$LOG_FILE"
clear
echo -e "${C}
▐▀▘ ▜▘▙ ▌▞▀▖▀▛▘▞▀▖▌  ▌  ▞▀▖▀▛▘▜▘▞▀▖▙ ▌ ▀▜ 
▐   ▐ ▌▌▌▚▄  ▌ ▙▄▌▌  ▌  ▙▄▌ ▌ ▐ ▌ ▌▌▌▌  ▐ 
▐   ▐ ▌▝▌▖ ▌ ▌ ▌ ▌▌  ▌  ▌ ▌ ▌ ▐ ▌ ▌▌▝▌  ▐ 
▝▀▘ ▀▘▘ ▘▝▀  ▘ ▘ ▘▀▀▘▀▀▘▘ ▘ ▘ ▀▘▝▀ ▘ ▘ ▀▀ ${N}"
echo ""
echo "Choose your operational system:"
echo -e "[ 1 ] Linux"
echo -e "[ 2 ] MacOS"
echo -e "[ 3 ] Windows"
read -p "> " option

REAL_OS=$(detect_system)

case "$option" in
1) TARGET_OS="Linux" ;;
2) TARGET_OS="MacOS" ;;
3) TARGET_OS="Windows" ;;
*)
  echo -e "${R}[ ✖ ] Invalid option.${N}"
  exit 1
  ;;
esac

if [ "$TARGET_OS" != "$REAL_OS" ] && [ "$TARGET_OS" != "Windows" ]; then
  echo -e "${Y}[ ! ] Warning: You chose $TARGET_OS but you are on $REAL_OS.${N}"
  read -p "Continue anyway? (y/n) " -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

if [ "$TARGET_OS" == "Windows" ]; then
  echo -e "${R}[ ✖ ] Please run 'install.ps1' on PowerShell.${N}"
  exit 0
fi

clear
echo -e "${C}
▐▀▘ ▛▀▖▛▀▖▞▀▖▞▀▖▛▀▘▞▀▖▞▀▖▜▘▙ ▌▞▀▖ ▀▜ 
▐   ▙▄▘▙▄▘▌ ▌▌  ▙▄ ▚▄ ▚▄ ▐ ▌▌▌▌▄▖  ▐ 
▐   ▌  ▌▚ ▌ ▌▌ ▖▌  ▖ ▌▖ ▌▐ ▌▝▌▌ ▌  ▐ 
▝▀▘ ▘  ▘ ▘▝▀ ▝▀ ▀▀▘▝▀ ▝▀ ▀▘▘ ▘▝▀  ▀▀ ${N}"
echo ""
echo -e "${C}[ ✓ ] Target: $TARGET_OS${N}"

(sleep 1) &
loader "Detecting Python..."
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo -e "${R}[ ✖ ] Python not found.${N}"
  echo "Check $LOG_FILE for details."
  exit 1
fi
echo -e "${G}[ ✓ ] Python found ($PY)${N}"

(sleep 1) &
loader "Detecting pipx..."
if command -v pipx >/dev/null 2>&1; then
  echo -e "${G}[ ✓ ] pipx found${N}"
else
  echo -e "${R}[ ✖ ] pipx not found.${N}"
  echo "Please install pipx first (e.g., sudo pacman -S python-pipx)"
  exit 1
fi

(run_safe pipx install . --force) &
PID_INSTALL=$!
loader "Installing passtw v1.0.0..."
wait $PID_INSTALL
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  clear
  echo -e "${G}
██████╗  █████╗ ███████╗████████╗███████╗██╗    ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║    ██║
██████╔╝███████║███████╗███████╗   ██║   ██║ █╗ ██║
██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██║███╗██║
██║     ██║  ██║███████║███████║   ██║   ╚███╔███╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚══╝╚══╝ ${N}"
  echo ""
  echo -e "${G}[ ✓ ] Successfully installed!${N}"
  echo -e "Run ${Y}passtw${N} to start."
  echo ""
else
  echo -e "${R}
[ ✖ ] Installation FAILED.${N}"
  echo "Check the log file for errors: $LOG_FILE"
  echo "Tip: Try running 'pipx uninstall passtw' and try again."
fi

