# C:\Users\baket\code\m2-miniweb\start-miniweb.ps1
param(
  [string]$Host = "127.0.0.1",
  [int]$Port = 8000
)
$PSScriptRoot | Out-Null
Set-Location $PSScriptRoot
.\.venv\Scripts\Activate.ps1
python ".\server.py" --host $Host --port $Port
