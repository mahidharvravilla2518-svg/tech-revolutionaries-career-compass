@echo off
setlocal
cd /d "%~dp0"
set "PYTHON=%LocalAppData%\Python\pythoncore-3.14-64\python.exe"
if not exist "%PYTHON%" (
  where py >nul 2>nul
  if not errorlevel 1 (
    set "PYTHON=py"
  ) else (
    where python >nul 2>nul
    if not errorlevel 1 (
      set "PYTHON=python"
    ) else (
      echo Python was not found. Install Python or open README.md for the known setup path.
      pause
      exit /b 1
    )
  )
)
"%PYTHON%" -c "import streamlit" >nul 2>nul
if errorlevel 1 (
  echo Installing the project requirements for the selected Python...
  "%PYTHON%" -m pip install -r requirements.txt
  if errorlevel 1 (
    echo Installation failed. Please copy the error and ask for help.
    pause
    exit /b 1
  )
)
"%PYTHON%" -m streamlit run app.py
if errorlevel 1 pause
endlocal
