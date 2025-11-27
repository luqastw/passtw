Set-ExecutionPolicy -Scope Process Bypass -Force
$ErrorActionPreference = "Stop"

function Start-Loader {
    param([string]$Message)

    $script:loaderRunning = $true

    Start-Job -ScriptBlock {
        param($Message)
        
        while ($true) {
            Write-Host "`r$Message.  " -NoNewline
            Start-Sleep -Milliseconds 300
            Write-Host "`r$Message.. " -NoNewline
            Start-Sleep -Milliseconds 300
            Write-Host "`r$Message..." -NoNewline
            Start-Sleep -Milliseconds 300
        }
    } -ArgumentList $Message | Set-Variable loaderJob
}

function Stop-Loader {
    if ($script:loaderRunning -and (Get-Job -Id $loaderJob.Id -ErrorAction SilentlyContinue)) {
        Stop-Job $loaderJob -Force | Out-Null
        Remove-Job $loaderJob -Force | Out-Null
    }
    Write-Host "`r" -NoNewline
    $script:loaderRunning = $false
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
Write-Host "[ ! ] Installing passtw for Windows."
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

if (-not $pipx) {
    Stop-Loader
    Write-Host "[ i ] pipx not found. Installing..." -ForegroundColor Yellow

    Start-Loader "[ 2 ] Installing pipx"

    Run-Silent { python -m pip install --user pipx }
    Run-Silent { python -m pipx ensurepath }

    Stop-Loader
    Write-Host "[ ✓ ] pipx installed." -ForegroundColor Green

    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","User") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH","Machine")

    $pipx = Get-Command pipx -ErrorAction SilentlyContinue
    if (-not $pipx) {
        Write-Host "[ ✖ ] pipx installation failed." -ForegroundColor Red
        exit 1
    }
} else {
    Stop-Loader
    Write-Host "[ ✓ ] pipx found." -ForegroundColor Green
}

Start-Loader "[ 3 ] Installing passtw"

Run-Silent { pipx install . }

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

Write-Host "[ ✓ ] Successfully installed!" -ForegroundColor Green
Write-Host "Type 'passtw init' to start."
Write-Host ""
