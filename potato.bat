@echo off
setlocal enabledelayedexpansion

:: User Configurable Variables
set ADDON_NAME=BPotato
set SOURCE_DIR=src
set DIST_DIR=dist
set DEFAULT_BLENDER_VERSION=4.3

:: Initialize paths
set ROOT_DIR=%~dp0
set BLENDER_BASE=%APPDATA%\Blender Foundation\Blender
set OPERATION=help

:: Get current Git branch
set GIT_BRANCH=unknown
git rev-parse --abbrev-ref HEAD 2>nul >nul && (
    for /f "delims=" %%b in ('git rev-parse --abbrev-ref HEAD') do set "GIT_BRANCH=%%b"
)

:: Parse command-line arguments
if not "%~1"=="" set OPERATION=%~1
if not "%~2"=="" set BLENDER_VERSION=%~2
if not defined BLENDER_VERSION set BLENDER_VERSION=%DEFAULT_BLENDER_VERSION%

:: Calculate full paths
set FULL_SOURCE=%ROOT_DIR%%SOURCE_DIR%
set FULL_DIST=%ROOT_DIR%%DIST_DIR%
set ADDON_INSTALL_DIR=%BLENDER_BASE%\%BLENDER_VERSION%\scripts\addons

:: Verify source directory exists
if not exist "%FULL_SOURCE%\" (
    echo Error: Source directory not found at %FULL_SOURCE%
    exit /b 1
)

:: Main command router
goto %OPERATION% 2>nul || goto help

:: Help documentation
:help
echo.
echo  BPotato Blender Addon - Build Script Help
echo  ========================================
echo  Location: %ROOT_DIR%
echo  Branch: !GIT_BRANCH!
echo.
echo  potato [command] [blender_version]
echo.
echo  Commands:
echo    package     - Build addon zip package
echo    install     - Install to specified Blender version
echo    uninstall   - Remove from Blender addons directory
echo    clean       - Clean build artifacts
echo    test        - Run code checks (requires flake8)
echo    dev         - Clean + package + install
echo    reload      - Uninstall + dev
echo.
echo  Blender Version:
echo    Default: %DEFAULT_BLENDER_VERSION%
echo    Current: %BLENDER_VERSION%
echo    Install path: %ADDON_INSTALL_DIR%
echo.
echo  Examples:
echo    potato install
echo    potato install 3.6
echo    potato uninstall 4.0
echo.
goto :eof

:: Clean build artifacts
:clean
echo.
echo  Cleaning build artifacts...
if exist "%FULL_DIST%" rmdir /s /q "%FULL_DIST%"
if exist "%FULL_SOURCE%\*.pyc" del /s /q "%FULL_SOURCE%\*.pyc"
echo  Done.
goto :eof

:: Build addon zip package
:package
call :clean
echo.
echo  Packaging addon [!GIT_BRANCH!]...
if not exist "%FULL_DIST%" mkdir "%FULL_DIST%"

:: Create zip file at: dist\BPotato_1.0.0.zip
set "ZIP_PATH=%FULL_DIST%\%ADDON_NAME%_!GIT_BRANCH!.zip"

python package.py "%FULL_SOURCE%" "%ZIP_PATH%"

if not exist "%ZIP_PATH%" (
    echo  Error: Failed to create zip package
    exit /b 1
)
echo  Created: %ZIP_PATH%
goto :eof

:: Install to Blender
:install
call :package
echo.
echo  Installing [!GIT_BRANCH!] to Blender %BLENDER_VERSION%...

:: Verify Blender directory exists
if not exist "%ADDON_INSTALL_DIR%" (
    echo  ERROR: Blender %BLENDER_VERSION% not found at:
    echo  "%ADDON_INSTALL_DIR%"
    echo  Please verify Blender version and installation
    exit /b 1
)

:: Install addon (preserve existing __init__.py)
if not exist "%ADDON_INSTALL_DIR%\%ADDON_NAME%" mkdir "%ADDON_INSTALL_DIR%\%ADDON_NAME%"
xcopy /Y /E /Q "%FULL_SOURCE%\*" "%ADDON_INSTALL_DIR%\%ADDON_NAME%\"

echo  Installed to: "%ADDON_INSTALL_DIR%\%ADDON_NAME%"
echo  Branch: !GIT_BRANCH!
echo  Please restart Blender to activate the addon
goto :eof

:: Remove from Blender
:uninstall
echo.
echo  Uninstalling from Blender %BLENDER_VERSION%...
set ADDON_PATH="%ADDON_INSTALL_DIR%\%ADDON_NAME%"

if exist %ADDON_PATH% (
    rmdir /s /q %ADDON_PATH%
    echo  Removed: %ADDON_PATH%
) else (
    echo  Addon not found: %ADDON_PATH%
)
goto :eof

:: Run code checks
:test
echo.
echo  Running code checks...
flake8 "%FULL_SOURCE%"
if errorlevel 1 (
    echo  Code checks failed
    exit /b 1
) else (
    echo  All tests passed!
)
goto :eof

:: Development shortcut
:dev
call :clean
call :install
echo.
echo  Development cycle complete for [!GIT_BRANCH!]!
goto :eof

:: Quickly Development shortcut
:reload
call :uninstall
call :clean
call :install
echo.
echo  Development cycle complete for [!GIT_BRANCH!]!
goto :eof

:: End of script
:eof
endlocal