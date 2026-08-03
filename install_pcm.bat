@echo off
REM Set Python 3.11 launcher explicitly
set PYTHON_EXE=py -3.11

REM Set virtual environment path
set VENV_PATH=%~dp0progress\env_pcm

REM Set path to cloned repo inside venv
set REPO_PATH=%VENV_PATH%\snl_quest_pcm

REM Remove existing cloned repo folder if exists
if exist "%REPO_PATH%" (
    echo Removing existing repo folder...
    rmdir /S /Q "%REPO_PATH%"
)

REM Create virtual environment (force recreate)
if exist "%VENV_PATH%" (
    echo Removing existing virtual environment...
    rmdir /S /Q "%VENV_PATH%"
)
echo Creating Python 3.11 virtual environment...
%PYTHON_EXE% -m venv "%VENV_PATH%"

REM Activate virtual environment
call "%VENV_PATH%\Scripts\activate.bat"

echo Ensuring pip is installed...
python -m ensurepip --upgrade

REM Verify pip works
python -m pip --version || (
    echo ERROR: pip is not working
    exit /b 1
)

REM Clone repo into the env folder
echo Cloning quest_PCM repo...
git clone -b progress_integration https://github.com/sandialabs/quest_PCM "%REPO_PATH%"

REM Install the package in editable mode
echo Installing quest_PCM package...
python -m pip install --upgrade pip
python -m pip install -e "%REPO_PATH%" || (
    echo ERROR: quest_PCM install failed
    exit /b 1
)

REM Deactivate virtual environment
deactivate

echo Setup complete.
exit /b 0