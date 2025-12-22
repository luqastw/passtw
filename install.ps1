Set-ExecutionPolicy -Scope Process Bypass -Force
$ErrorActionPreference = "Stop"

function Start-Loader {
    param([string]$Message)

    if ($script:loaderRunning) { return }

    $script:loaderRunning = $true

    $script:loaderJob = Start-ThreadJob -ScriptBlock {
        param($Message)
$ErrorActionPreference = "Stop"
$LogFile = "install.log"
$host.UI.RawUI.WindowTitle = "Installer"

if (Test-Path $LogFile) { Remove-Item $LogFile -Force }

function Invoke-WithSpinner {
    param (
        [string]$Message,
        [ScriptBlock]$Action
    )

    $spins = "|", "/", "-", "\"
    $spinIndex = 0
    
    $job = Start-Job -ScriptBlock $Action
    
    [Console]::CursorVisible = $false
    
    try {
        while ($job.State -eq 'Running') {
            $spinChar = $spins[$spinIndex % $spins.Count]
            Write-Host -NoNewline " [$spinChar] $Message"
            
            Start-Sleep -Milliseconds 100
            
            $cursorPos = [Console]::CursorLeft
            if ($cursorPos -gt 0) {
                [Console]::SetCursorPosition(0, [Console]::CursorTop)
            }
            
            $spinIndex++
        }
        
        $results = Receive-Job $job
        $results | Out-File $LogFile -Append -Encoding UTF8
        
        Write-Host (" " * 60) -NoNewline
        [Console]::SetCursorPosition(0, [Console]::CursorTop)

        return $job.ChildJobs[0].ExitCode
    }
    finally {
        [Console]::CursorVisible = $true
        Remove-Job $job -Force
    }
}

Clear-Host
Write-Host @"
▐▀▘ ▜▘▙ ▌▞▀▖▀▛▘▞▀▖▌  ▌  ▞▀▖▀▛▘▜▘▞▀▖▙ ▌ ▀▜ 
▐   ▐ ▌▌▌▚▄  ▌ ▙▄▌▌  ▌  ▙▄▌ ▌ ▐ ▌ ▌▌▌▌  ▐ 
▐   ▐ ▌▝▌▖ ▌ ▌ ▌ ▌▌  ▌  ▌ ▌ ▌ ▐ ▌ ▌▌▝▌  ▐ 
▝▀▘ ▀▘▘ ▘▝▀  ▘ ▘ ▘▀▀▘▀▀▘▘ ▘ ▘ ▀▘▝▀ ▘ ▘ ▀▀ 
"@ -ForegroundColor Cyan

Write-Host "`nChoose your operational system:"
Write-Host "[ 1 ] Linux"
Write-Host "[ 2 ] MacOS"
Write-Host "[ 3 ] Windows"
$option = Read-Host "> "

$RealOS = if ($IsWindows -or $env:OS -match "Windows") { "Windows" } else { "Unix-like" }
$TargetOS = ""

switch ($option) {
    "1" { $TargetOS = "Linux" }
    "2" { $TargetOS = "MacOS" }
    "3" { $TargetOS = "Windows" }
    Default {
        Write-Host "[ ✖ ] Invalid option." -ForegroundColor Red
        exit 1
    }
}

if ($TargetOS -ne "Windows") {
    Write-Host "[ ! ] Warning: You chose $TargetOS but you are on Windows." -ForegroundColor Yellow
    $confirm = Read-Host "Continue anyway? (y/n)"
    if ($confirm -notmatch "^[Yy]") { exit 1 }
}

Clear-Host
Write-Host @"
▐▀▘ ▛▀▖▛▀▖▞▀▖▞▀▖▛▀▘▞▀▖▞▀▖▜▘▙ ▌▞▀▖ ▀▜ 
▐   ▙▄▘▙▄▘▌ ▌▌  ▙▄ ▚▄ ▚▄ ▐ ▌▌▌▌▄▖  ▐ 
▐   ▌  ▌▚ ▌ ▌▌ ▖▌  ▖ ▌▖ ▌▐ ▌▝▌▌ ▌  ▐ 
▝▀▘ ▘  ▘ ▘▝▀ ▝▀ ▀▀▘▝▀ ▝▀ ▀▘▘ ▘▝▀  ▀▀ 
"@ -ForegroundColor Cyan

Write-Host "`n[ ✓ ] Target: $TargetOS" -ForegroundColor Cyan

Start-Sleep -Seconds 1
Invoke-WithSpinner "Detecting Python..." { Start-Sleep -Milliseconds 500 } | Out-Null

if (Get-Command "python" -ErrorAction SilentlyContinue) {
    $PY = "python"
} elseif (Get-Command "python3" -ErrorAction SilentlyContinue) {
    $PY = "python3"
} else {
    Write-Host "[ ✖ ] Python not found." -ForegroundColor Red
    Write-Host "Check $LogFile for details."
    exit 1
}
Write-Host "[ ✓ ] Python found ($PY)" -ForegroundColor Green

Start-Sleep -Seconds 1
Invoke-WithSpinner "Detecting pipx..." { Start-Sleep -Milliseconds 500 } | Out-Null

if (Get-Command "pipx" -ErrorAction SilentlyContinue) {
    Write-Host "[ ✓ ] pipx found" -ForegroundColor Green
} else {
    Write-Host "[ ✖ ] pipx not found." -ForegroundColor Red
    Write-Host "Please install pipx first (e.g., winget install pipx)"
    exit 1
}

$ExitCode = Invoke-WithSpinner "Installing passtw v1.0.0..." {
    pipx install . --force 2>&1
}

if ($ExitCode -eq 0 -or $LASTEXITCODE -eq 0) {
    Clear-Host
    Write-Host @"
██████╗  █████╗ ███████╗████████╗███████╗██╗    ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║    ██║
██████╔╝███████║███████╗███████╗   ██║   ██║ █╗ ██║
██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██║███╗██║
██║     ██║  ██║███████║███████║   ██║   ╚███╔███╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚══╝╚══╝ 
"@ -ForegroundColor Green
    
    Write-Host "`n[ ✓ ] Successfully installed!" -ForegroundColor Green
    Write-Host "Run 'passtw' to start." -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "`n[ ✖ ] Installation FAILED." -ForegroundColor Red
    Write-Host "Check the log file for errors: $LogFile"
    Write-Host "Tip: Try running 'pipx uninstall passtw' and try again."
}
