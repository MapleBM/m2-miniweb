# m2-miniweb

Tiny stdlib web app:
- Static UI at `/` from `web/`
- JSON API: `/api/echo?msg=hello` → `{"msg":"hello","length":5}`
- Logs rotate in `.\logs\web.log`

## Run (Windows, PowerShell)
```powershell
# from project root with venv active
python ".\server.py" --host 127.0.0.1 --port 8000
# or use the helper script:
.\start-miniweb.ps1 -Port 9000
