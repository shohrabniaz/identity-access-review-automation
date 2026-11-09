Set-Location (Split-Path -Parent $PSScriptRoot)
python -m src.cli review --path .\data\entitlements.csv
python tests\test_smoke.py
