#!/bin/bash

detect_system() {
    local os="$(uname -s)"

    case "$os" in
        Linux)   echo "linux" ;;
        Darwin)  echo "macos" ;;
        *)       echo "windows" ;;
    esac
}

loader() {
    local msg="$1"
    while :; do
        printf "\r%s.  " "$msg"; sleep 0.3
        printf "\r%s.. " "$msg"; sleep 0.3
        printf "\r%s..." "$msg"; sleep 0.3
    done
}

run_silent() {
    "$@" > /dev/null 2>&1
}

clear
echo "                                                                                                                                                                                          
▐▀▘ ▜▘▙ ▌▞▀▖▀▛▘▞▀▖▌  ▌  ▞▀▖▀▛▘▜▘▞▀▖▙ ▌ ▀▜ 
▐   ▐ ▌▌▌▚▄  ▌ ▙▄▌▌  ▌  ▙▄▌ ▌ ▐ ▌ ▌▌▌▌  ▐ 
▐   ▐ ▌▝▌▖ ▌ ▌ ▌ ▌▌  ▌  ▌ ▌ ▌ ▐ ▌ ▌▌▝▌  ▐ 
▝▀▘ ▀▘▘ ▘▝▀  ▘ ▘ ▘▀▀▘▀▀▘▘ ▘ ▘ ▀▘▝▀ ▘ ▘ ▀▀ "
echo ""
echo "Choose your operational system:"
echo "[ 1 ] Linux"
echo "[ 2 ] MacOs"
echo "[ 3 ] Windows"
read -p "> " option

REAL_OS=$(detect_system)

case "$option" in
    1) USER_OS="linux" ;;
    2) USER_OS="macos" ;;
    3) USER_OS="windows" ;;
    *)
        clear
        echo "[ ✖ ] Invalid option. Please choose 1, 2, or 3."
        exit 1
        ;;
esac

if [ "$USER_OS" != "$REAL_OS" ]; then
    clear
    echo "[ ✖ ] The chosen system does not match your real OS."
    echo "      → You chose: $USER_OS"
    echo "      → Real OS:   $REAL_OS"
    echo ""
    exit 1
fi

case "$option" in
    1)
        clear
        echo "
▐▀▘ ▛▀▖▛▀▖▞▀▖▞▀▖▛▀▘▞▀▖▞▀▖▜▘▙ ▌▞▀▖ ▀▜ 
▐   ▙▄▘▙▄▘▌ ▌▌  ▙▄ ▚▄ ▚▄ ▐ ▌▌▌▌▄▖  ▐ 
▐   ▌  ▌▚ ▌ ▌▌ ▖▌  ▖ ▌▖ ▌▐ ▌▝▌▌ ▌  ▐ 
▝▀▘ ▘  ▘ ▘▝▀ ▝▀ ▀▀▘▝▀ ▝▀ ▀▘▘ ▘▝▀  ▀▀ "
        echo ""
        echo "[ ✓ ] OS selected: Linux"
        loader "[ 1 ] Detecting Python" &
        LOADER_PID=$!
        if run_silent command -v python3; then
            kill "$LOADER_PID" >/dev/null 2>&1
            PY=python3
        elif run_silent command -v python; then
            kill "$LOADER_PID" >/dev/null 2>&1
            PY=python
        else
            kill "$LOADER_PID" >/dev/null 2>&1
            printf "\r%-40s\r" 
            echo "[ ✖ ] Python not found."
            exit 1
        fi

        printf "\r%-40s\r" 
        echo "[ ✓ ] Python found."

        loader "[ 2 ] Detecting pipx" &
        LOADER_PID=$!
        if run_silent command -v pipx; then
            kill "$LOADER_PID" >/dev/null 2>&1
            printf "\r%-40s\r" 
            echo "[ ✓ ] pipx found."
        else
            kill "$LOADER_PID" >/dev/null 2>&1
            printf "\r%-40s\r" 
            echo "[ ✖ ] pipx not found."
            exit 1
        fi

        loader "[ 3 ] Installing passtw" &
        LOADER_PID=$!
        run_silent pipx install .
        kill "$LOADER_PID" >/dev/null 2>&1
        clear

        echo "
██████╗  █████╗ ███████╗███████╗████████╗██╗    ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║    ██║
██████╔╝███████║███████╗███████╗   ██║   ██║ █╗ ██║
██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██║███╗██║
██║     ██║  ██║███████║███████║   ██║   ╚███╔███╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚══╝╚══╝ 
        "
        echo "[ ✓ ] Succefully installed!"
        echo "Type passtw init to start."
        echo ""
        ;;

    2) 
        clear
        echo "
▐▀▘ ▛▀▖▛▀▖▞▀▖▞▀▖▛▀▘▞▀▖▞▀▖▜▘▙ ▌▞▀▖ ▀▜ 
▐   ▙▄▘▙▄▘▌ ▌▌  ▙▄ ▚▄ ▚▄ ▐ ▌▌▌▌▄▖  ▐ 
▐   ▌  ▌▚ ▌ ▌▌ ▖▌  ▖ ▌▖ ▌▐ ▌▝▌▌ ▌  ▐ 
▝▀▘ ▘  ▘ ▘▝▀ ▝▀ ▀▀▘▝▀ ▝▀ ▀▘▘ ▘▝▀  ▀▀ "
        echo ""
        echo "[ ✓ ] OS selected: MacOs"
        loader "[ 1 ] Detecting Python" &
        LOADER_PID=$!
        if run_silent command -v python3; then
            kill "$LOADER_PID" >/dev/null 2>&1
            PY=python3
        elif run_silent command -v python; then
            kill "$LOADER_PID" >/dev/null 2>&1
            PY=python
        else
            kill "$LOADER_PID" >/dev/null 2>&1
            echo "[ ✖ ] Python not found."
            exit 1
        fi

        printf "\r%-40s\r" 
        echo "[ ✓ ] Python found."

        loader "[ 2 ] Detecting pipx" &
        LOADER_PID=$!
        if run_silent command -v pipx; then
            kill "$LOADER_PID" >/dev/null 2>&1
            printf "\r%-40s\r" 
            echo "[ ✓ ] pipx found."
        else
            kill "$LOADER_PID" >/dev/null 2>&1
            printf "\r%-40s\r" 
            echo "[ ✖ ] pipx not found."
            exit 1
        fi

        loader "[ 3 ] Installing passtw" &
        LOADER_PID=$!
        run_silent pipx install .
        kill "$LOADER_PID" >/dev/null 2>&1
        clear

        echo "
██████╗  █████╗ ███████╗███████╗████████╗██╗    ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║    ██║
██████╔╝███████║███████╗███████╗   ██║   ██║ █╗ ██║
██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██║███╗██║
██║     ██║  ██║███████║███████║   ██║   ╚███╔███╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚══╝╚══╝ 
        "
        echo "[ ✓ ] Succefully installed!"
        echo "Type passtw init to start."
        echo""
        ;;
    
    3)
        clear
        echo "
▐▀▘ ▙ ▌▞▀▖▀▛▘ ▞▀▖▌ ▌▞▀▖▜▘▌  ▞▀▖▛▀▖▌  ▛▀▘ ▀▜ 
▐   ▌▌▌▌ ▌ ▌  ▙▄▌▚▗▘▙▄▌▐ ▌  ▙▄▌▙▄▘▌  ▙▄   ▐ 
▐   ▌▝▌▌ ▌ ▌  ▌ ▌▝▞ ▌ ▌▐ ▌  ▌ ▌▌ ▌▌  ▌    ▐ 
▝▀▘ ▘ ▘▝▀  ▘  ▘ ▘ ▘ ▘ ▘▀▘▀▀▘▘ ▘▀▀ ▀▀▘▀▀▘ ▀▀ "
        echo ""
        echo "[ ✖ ] Stay tuned for any new updates until available."
        echo ""
        ;;
esac