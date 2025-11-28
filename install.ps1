Set-ExecutionPolicy -Scope Process Bypass -Force
$ErrorActionPreference = "Stop"

function Start-Loader {
    param([string]$Message)

    if ($script:loaderRunning) { return }

    $script:loaderRunning = $true

    $script:loaderJob = Start-Job -ScriptBlock {
        param($Message)
        while ($true) {
            Write-Host "`r$Message.  " -NoNewline
            Start-Sleep -Milliseconds 250
            Write-Host "`r$Message.. " -NoNewline
            Start-Sleep -Milliseconds 250
            Write-Host "`r$Message..." -NoNewline
            Start-Sleep -Milliseconds 250
        }
    } -ArgumentList $Message
}

function Stop-Loader {
    if ($script:loaderRunning -and $script:loaderJob) {
        if (Get-Job -Id $script:loaderJob.Id -ErrorAction SilentlyContinue) {
            Stop-Job $script:loaderJob -Force -ErrorAction SilentlyContinue | Out-Null
            Remove-Job $script:loaderJob -Force -ErrorAction SilentlyContinue | Out-Null
        }
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
▐▀▘ ▜▘▙ ▌▞▀▖▀▛▘▞▀▖▌  ▌  ▞▀▖▀▛▘▜▘▞▀▖▙ ▌ ▀▜ 
▐   ▐ ▌▌▌▚▄  ▌ ▙▄▌▌  ▌  ▙▄▌ ▌ ▐ ▌ ▌▌▌▌  ▐ 
▐   ▐ ▌▝▌▖ ▌ ▌ ▌ ▌▌  ▌  ▌ ▌ ▌ ▐ ▌ ▌▌▝▌  ▐ 
▝▀▘ ▀▘▘ ▘▝▀  ▘ ▘ ▘▀▀▘▀▀▘▘ ▘ ▘ ▀▘▝▀ ▘ ▘ ▀▀ 
" -ForegroundColor Cyan

Write-Host ""
Write-Host "[ * ] Installing passtw for Windows."
Write-Host ""

Start-Loader "[ 1 ] Detecting Python"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $python) {
    Stop-Loader
    Write-Host "[ ✖ ] Python not found." -ForegroundColor Red
    exit 1
}

Stop-Loader
Write-Host "[ ✓ ] Python found." -ForegroundColor Green
$PY = $python.Source

Start-Loader "[ 2 ] Detecting pipx"

$pipx = Get-Command pipx -ErrorAction SilentlyContinue

Stop-Loader

if (-not $pipx) {
    Write-Host "[ i ] pipx not found. Installing..." -ForegroundColor Yellow

    Start-Loader "[ 2 ] Installing pipx"

    Run-Silent { & $using:PY -m pip install --user pipx }
    Run-Silent { & $using:PY -m pipx ensurepath }

    Stop-Loader
    Write-Host "[ ✓ ] pipx installed." -ForegroundColor Green

    $PipxBin = "$env:USERPROFILE\.local\bin"
    if (-not ($env:PATH -split ";" | Where-Object { $_ -eq $PipxBin })) {
        $env:PATH += ";$PipxBin"
    }

    $pipx = Get-Command pipx -ErrorAction SilentlyContinue
    if (-not $pipx) {
        Write-Host "[ ✖ ] pipx installation failed." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[ ✓ ] pipx found." -ForegroundColor Green
}

Start-Loader "[ 3 ] Installing passtw"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Run-Silent { pipx install $using:ScriptDir }

Stop-Loader

if (-not (Get-Command passtw -ErrorAction SilentlyContinue)) {
    Write-Host "[ ✖ ] passtw not found. Install failed." -ForegroundColor Red
    exit 1
}

Clear-Host
Write-Host "
██████╗  █████╗ ███████╗███████╗████████╗██╗    ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║    ██║
██████╔╝███████║███████╗███████╗   ██║   ██║ █╗ ██║
██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██║███╗██║
██║     ██║  ██║███████║███████║   ██║   ╚███╔███╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚══╝╚══╝ 
" -ForegroundColor Cyan

Write-Host "[ ✓ ] Successfully installed." -ForegroundColor Green
Write-Host "Type passtw init to start."
Write-Host ""
