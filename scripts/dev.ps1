# Arranque local MD-PDF (requiere .venv creado e instalado)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Error "No existe .venv. Ejecutá: python -m venv .venv ; .\.venv\Scripts\Activate.ps1 ; pip install -r requirements.txt ; playwright install chromium"
}

& $Python run.py @args
