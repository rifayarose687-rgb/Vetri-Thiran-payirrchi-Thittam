# PocketSmart AI

A small FastAPI application. The current root endpoint returns `{"message":"Hello World"}`.

## Requirements

- Python 3.11 or newer
- PowerShell on Windows

## Run locally

From the project folder, run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000> to view the app. Interactive API documentation is at <http://127.0.0.1:8000/docs>.

To stop the server, press `Ctrl+C` in the PowerShell terminal running Uvicorn.

## Configuration

`.env.example` contains sample settings. Copy it to the location required by your configuration before adding any credentials. Do not share real API keys or secrets in the project archive.