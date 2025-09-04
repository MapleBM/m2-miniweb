\# m2-miniweb



Tiny stdlib web app:

\- Serves `/` from `web/` (HTML/CSS/JS)

\- JSON API: `/api/echo?msg=hello` → `{"msg":"hello","length":5}`



\## Run (Windows, PowerShell)

```powershell

\# from project root with venv active

python "C:\\Users\\baket\\code\\m2-miniweb\\server.py" --host 127.0.0.1 --port 8000

\# then open: http://127.0.0.1:8000/api/echo?msg=hello



