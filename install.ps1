Set-ExecutionPolicy -Scope Process Bypass -Force
$ErrorActionPreference = "Stop"

function Start-Loader {
    param([string]$Message)

    if ($script:loaderRunning) { return }

    $script:loaderRunning = $true

    $script:loaderJob = Start-Job -ScriptBlock {
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

Write-Host ""
Write-Host "Installing passtw for Windows."
Write-Host ""

Start-Loader "Detecting Python"

$python = Get-Command python -ErrorAction Silen
