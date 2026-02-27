Set-ExecutionPolicy -Scope Process Bypass -Force
$ErrorActionPreference = "Stop"

$LogFile = "install.log"
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
            Write-Host -NoNewline "`r [$spinChar] $Message"
            Start-Sleep -Milliseconds 100
            $spinIndex++
        }
        
        $results = Receive-Job $job
        if ($results) { $results | Out-File $LogFile -Append -Encoding UTF8 }
        Write-Host -NoNewline "`r" + (" " * 70) + "`r"
        return $job.ChildJobs[0].ExitCode
    }
    finally {
        [Console]::CursorVisible = $true
        Remove-Job $job -Force
    }
}

Clear-Host
Write-Host @"
▐▀▘ ▜▘▙ ▌▞▀▖▀▛▘▞▀▖▌   ▌  ▞▀▖▀▛▘▜▘▞▀▖▙ ▌ ▀▜ 
▐   ▐ ▌▌▌▚▄  ▌ ▙▄▌▌   ▌  ▙▄▌ ▌ ▐ ▌ ▌▌▌▌  ▐ 
▐   ▐ ▌▝▌▖ ▌ ▌ ▌ ▌▌   ▌  ▌ ▌ ▌ ▐ ▌ ▌▌▝▌  ▐ 
▝▀▘ ▀▘▘ ▘▝▀  ▘ ▘ ▘▀▀▘▀▀▘▘ ▘ ▘ ▀▘▝▀ ▘ ▘ ▀▀ 
"@ -ForegroundColor Cyan

Write-Host "`nChoose your operational system:"
Write-Host "[ 1 ] Linux"
Write-Host "[ 2 ] MacOS"
Write-Host "[ 3 ] Windows"
$option = Read-Host "> "

switch ($option) {
    "1" { $TargetOS = "Linux" }
    "2" { $TargetOS = "MacOS" }
    "3" { $TargetOS = "Windows" }
    Default {
        Write-Host "[ X ] Invalid option." -ForegroundColor Red
        exit 1
    }
}

Clear-Host
Write-Host @"
▐▀▘ ▛▀▖▛▀▖▞▀▖▞▀▖▛▀▘▞▀▖▞▀▖▜▘▙ ▌▞▀▖ ▀▜ 
▐   ▙▄▘▙▄▘▌ ▌▌  ▙▄ ▚▄ ▚▄ ▐ ▌▌▌▌▄▖  ▐ 
▐   ▌  ▌▚ ▌ ▌▌ ▖▌  ▖ ▌▖ ▌▐ ▌▝▌▌ ▌  ▐ 
▝▀▘ ▘  ▘ ▘▝▀ ▝▀ ▀▀▘▝▀ ▝▀ ▀▘▘ ▘▝▀  ▀▀ 
"@ -ForegroundColor Cyan

Write-Host "`n[ OK ] Target: $TargetOS" -ForegroundColor Cyan

Invoke-WithSpinner "Detecting Python..." { 
    if (Get-Command "python" -ErrorAction SilentlyContinue) { return "python" }
    if (Get-Command "python3" -ErrorAction SilentlyContinue) { return "python3" }
    throw "Python not found"
} | Out-Null

if (Get-Command "python" -ErrorAction SilentlyContinue) { $PY = "python" }
else { $PY = "python3" }
Write-Host "[ OK ] Python found ($PY)" -ForegroundColor Green

if (Get-Command "pipx" -ErrorAction SilentlyContinue) {
    Write-Host "[ OK ] pipx found" -ForegroundColor Green
} else {
    Write-Host "[ X ] pipx not found." -ForegroundColor Red
    Write-Host "Please install pipx first (e.g., winget install pipx)"
    exit 1
}

Write-Host "Installing passtw v1.2.1..." -ForegroundColor Yellow
$ExitCode = Invoke-WithSpinner "Running pipx install..." {
    pipx install . --force
}

if ($LASTEXITCODE -eq 0) {
    Clear-Host
    Write-Host @"
██████╗  █████╗ ███████╗████████╗███████╗██╗    ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║    ██║
██████╔╝███████║███████╗███████╗   ██║   ██║ █╗ ██║
██╔═══╝ ██╔══██║╚════██║╚════██║   ██║   ██║███╗██║
██║     ██║  ██║███████║███████║   ██║   ╚███╔███╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚══╝╚══╝ 
"@ -ForegroundColor Green
    
    Write-Host "`n[ OK ] Successfully installed!" -ForegroundColor Green
    Write-Host "Run 'passtw' to start." -ForegroundColor Yellow
} else {
    Write-Host "`n[ X ] Installation FAILED." -ForegroundColor Red
    Write-Host "Check the log file for errors: $LogFile"
}