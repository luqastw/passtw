Set-ExecutionPolicy -Scope Process Bypass -Force
$ErrorActionPreference = "Stop"

function Start-Loader {
    param([string]$Message)

    if ($script:loaderRunning) { return }

    $script:loaderRunning = $true

    $script:loaderJob = Start-ThreadJob -ScriptBlock {
        param($Message)
        while ($true) {
            Write-Host "`r$Message... " -NoNewline
            Start-Sleep -Milliseconds 300
            Write-Host "`r$Message..  " -NoNewline
            Start-Sleep -Milliseconds 300
            Write-Host "`r$Message.   " -NoNewline
            Start-Sleep -Milliseconds 300
        }
    } -ArgumentList $Message
}

function Stop-Loader {
    if ($script:loaderRunning -and $script:loaderJob) {
        Stop-Job $script:loaderJob -ErrorAction SilentlyContinue | Out-Null
        Remove-Job $script:loaderJob -ErrorAction SilentlyContinue | Out-Null
    }

    Write-Host "`r`e[2K" -NoNewline

    $script:loaderRunning = $false
    $script:loaderJob = $null
}

function Run-Silent {
    param([scriptblock]$cmd)
    & $cmd *> $null 2>&1
    return $?
}

Clear-Host

Write-Host "
▐▀▘ ▛▀▖▛▀▖▞▀▖▞▀▖▛▀▘▞▀▖▞▀▖▜▘▙ ▌▞▀▖ ▀▜ 
▐   ▙▄▘▙▄▘▌ ▌▌  ▙▄ ▚▄ ▚▄ ▐ ▌▌▌▌▄▖  ▐ 
▐   ▌  ▌▚ ▌ ▌▌ ▖▌  ▖ ▌▖ ▌▐ ▌▝▌▌ ▌  ▐ 
▝▀▘ ▘  ▘ ▘▝▀ ▝▀ ▀▀▘▝▀ ▝▀ ▀▘▘ ▘▝▀  ▀▀ "
Write-Host ""
Write-Host "Installing passtw for Windows."
Write-Host ""

Start-Loader "Detecting Python"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $python) {
    Stop-Loader
    Write-Host "ERROR: Python not found."
    exit 1
}

Stop-Loader
Write-Host "Python detected."
$PY = $python.Source

Start-Loader "Detecting pipx"

$pipx = Get-Command pipx -ErrorAction SilentlyContinue

Stop-Loader

if (-not $pipx) {
    Write-Host "pipx not found. Installing..."

    Start-Loader "Installing pipx"

    Run-Silent { & $PY -m pip install --user pipx }
    Run-Silent { & $PY -m pipx ensurepath }

    Stop-Loader
    Write-Host "pipx installed."

    # Caminho real do pipx no Windows
    $PipxBin = "$env:USERPROFILE\AppData\Roaming\Python\Scripts"
    if (-not ($env:PATH -split ";" | Where-Object { $_ -eq $PipxBin })) {
        $env:PATH += ";$PipxBin"
    }

    $pipx = Get-Command pipx -ErrorAction SilentlyContinue
    if (-not $pipx) {
        Write-Host "ERROR: pipx installation failed."
        exit 1
    }
} else {
    Write-Host "pipx detected."
}

Start-Loader "Installing passtw"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# instala do diretório local
Run-Silent { pipx install $ScriptDir --force }

Stop-Loader

# Teste final
$passtwCheck = Get-Command passtw -ErrorAction SilentlyContinue
if (-not $passtwCheck) {
    Write-Host "WARNING: passtw not available in PATH in this session."
    Write-Host "Try opening a new terminal OR run:"
    Write-Host ""
    Write-Host "    refreshenv"
    Write-Host ""
} else {
    Write-Host "passtw detected."
}

Clear-Host
Write-Host "
██████╗  █████╗ ███████╗███████╗████████╗██╗    ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║    ██║
██████╔╝███████║███████╗███████╗   ██║   ██║ █╗ ██║
██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██║███╗██║
██║     ██║  ██║███████║███████║   ██║   ╚███╔███╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚══╝╚══╝ 
"
Write-Host "Installed successfully."
Write-Host "Run passtw init to start."
Write-Host ""
