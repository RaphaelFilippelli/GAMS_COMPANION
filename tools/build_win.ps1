
param(
  [switch]$Rebuild
)

if ($Rebuild) {
  if (Test-Path .venv) { Remove-Item -Recurse -Force .venv }
}

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$env:GAMS_HOME = $env:GAMS_HOME
if (-not $env:GAMS_HOME) { $env:GAMS_HOME = "C:\GAMS\44" }
Write-Host "GAMS_HOME = $env:GAMS_HOME"
