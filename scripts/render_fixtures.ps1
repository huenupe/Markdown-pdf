# Genera PDFs de fixtures/ en output/ (servidor levantado; default puerto 8765)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Port = if ($env:PORT) { $env:PORT } else { "8765" }
$Base = if ($env:MD_PDF_BASE) { $env:MD_PDF_BASE } else { "http://127.0.0.1:$Port" }

$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Error "No existe .venv. Creá el entorno e instalá deps (docs/03-SETUP.md)."
}

& $Python -c @"
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

root = Path(r'$Root')
base = os.environ.get('MD_PDF_BASE', r'$Base')
out_dir = root / 'output'
out_dir.mkdir(exist_ok=True)

for path in sorted((root / 'fixtures').glob('*.md')):
    payload = json.dumps(
        {'markdown': path.read_text(encoding='utf-8'), 'filename': path.name}
    ).encode('utf-8')
    req = urllib.request.Request(
        f'{base}/api/convert',
        data=payload,
        headers={'Content-Type': 'application/json'},
    )
    dest = out_dir / f'{path.stem}.pdf'
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
    except urllib.error.HTTPError as exc:
        raise SystemExit(f'{path.name}: HTTP {exc.code} {exc.read().decode()}') from exc
    if not data.startswith(b'%PDF'):
        raise SystemExit(f'{path.name}: respuesta no es PDF')
    dest.write_bytes(data)
    print(f'OK {path.name} -> {dest.name} ({len(data)} bytes)')
"@
