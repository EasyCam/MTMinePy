@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo === MTMinePy PyPI Upload Script ===

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: python is not installed or not in PATH.
    exit /b 1
)

REM Install build dependencies if missing
echo Installing/upgrading build tools...
python -m pip install --upgrade build twine

REM Clean previous builds
echo Cleaning old build artifacts...
if exist dist rd /s /q dist
if exist build rd /s /q build
for /d %%d in (*.egg-info) do rd /s /q "%%d"

REM Build the package
echo Building package...
python -m build
if %errorlevel% neq 0 (
    echo Error: Build failed.
    exit /b 1
)

REM Show built files
echo.
echo Built packages:
dir /b dist\

REM Choose upload target
echo.
set /p choice="Upload to [1] PyPI (default) or [2] TestPyPI? "

if "%choice%"=="2" (
    echo Uploading to TestPyPI...
    python -m twine upload --repository testpypi dist\*
    echo.
    echo Done! View at: https://test.pypi.org/project/mtminepy/
) else (
    echo Uploading to PyPI...
    python -m twine upload dist\*
    echo.
    echo Done! View at: https://pypi.org/project/mtminepy/
)

endlocal
