$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $projectRoot "backend"
$frontendPath = Join-Path $projectRoot "frontend"
$venvActivate = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $backendPath)) {
    throw "Backend folder not found: $backendPath"
}

if (-not (Test-Path $frontendPath)) {
    throw "Frontend folder not found: $frontendPath"
}

$backendCommand = @"
Set-Location '$projectRoot'
if (Test-Path '$venvActivate') { & '$venvActivate' }
Set-Location '$backendPath'
python main.py run-api
"@

$frontendCommand = @"
Set-Location '$frontendPath'
if (-not (Test-Path 'node_modules')) { npm install }
npm run dev
"@

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command", $backendCommand
) | Out-Null

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command", $frontendCommand
) | Out-Null

Start-Process "http://localhost:5173" | Out-Null

Write-Host "Started backend and frontend in separate windows."
Write-Host "Backend: http://127.0.0.1:5000"
Write-Host "Frontend: http://localhost:5173"
