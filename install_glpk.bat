@echo off
where glpsol >nul 2>&1
if %errorlevel%==0 (
    echo glpsol already installed.
    exit /b 0
)

echo glpsol not found. Downloading GLPK...
set URL=https://sourceforge.net/projects/winglpk/files/winglpk/GLPK-4.65/winglpk-4.65.zip/download
set TMPDIR=%TEMP%\glpk_install
mkdir %TMPDIR% 2>nul

curl -L --insecure -o "%TMPDIR%\glpk.zip" "%URL%"
if %errorlevel% neq 0 (
    echo Failed to download GLPK
    exit /b 1
)

powershell -Command "Expand-Archive -Path '%TMPDIR%\glpk.zip' -DestinationPath '%TMPDIR%\glpk' -Force"

if not exist "%USERPROFILE%\glpk" mkdir "%USERPROFILE%\glpk"
copy "%TMPDIR%\glpk\w64\glpsol.exe" "%USERPROFILE%\glpk\glpsol.exe"
copy "%TMPDIR%\glpk\w64\glpk.dll" "%USERPROFILE%\glpk\glpk.dll"

echo.
echo GLPK installed to %USERPROFILE%\glpk
echo Add this to your PATH: %USERPROFILE%\glpk

rd /s /q %TMPDIR%
