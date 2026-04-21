param(
    [ValidateSet("setup", "test", "run")]
    [string]$Task = "test"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

function Assert-Python {
    if (-not (Test-Path $VenvPython)) {
        throw "Virtual environment not found. Run: .\dev.ps1 setup"
    }
}

switch ($Task) {
    "setup" {
        $SystemPython = "C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe"
        if (-not (Test-Path $SystemPython)) {
            throw "Python 3.11 was not found at $SystemPython"
        }

        if (-not (Test-Path $VenvPython)) {
            & $SystemPython -m venv (Join-Path $Root ".venv")
        }

        & $VenvPython -m pip install --upgrade pip
        & $VenvPython -m pip install -r (Join-Path $Root "requirements.txt")

        if (-not (Test-Path (Join-Path $Root ".env"))) {
            "DATABASE_URL=sqlite:///./test.db" | Set-Content -Path (Join-Path $Root ".env")
        }
    }
    "test" {
        Assert-Python
        Push-Location $Root
        try {
            & $VenvPython -m pytest -q
        }
        finally {
            Pop-Location
        }
    }
    "run" {
        Assert-Python
        Push-Location $Root
        try {
            & $VenvPython -m uvicorn app.main:app --reload
        }
        finally {
            Pop-Location
        }
    }
}
