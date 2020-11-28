@echo off
set curpath=%~dp0

set UID=48140

rem cd ..
rem set KBE_ROOT=%cd%
rem set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
rem set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/
set KBE_ROOT=D:\TheWorld\KBEngine\kbengine\
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/

if defined uid (echo UID = %uid%)

cd %curpath%
rem call "kill_server.bat"

echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%

"%KBE_BIN_PATH%/kbcmd.exe" --getuid > nul
if not defined uid set uid=%errorlevel%
echo UID = %uid%

set PYTHON="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python"
if defined KBE_ROOT (%PYTHON% "%KBE_ROOT%/kbe\tools\server\pycluster\cluster_controller.py" shutdown %uid%) else (%PYTHON% "..\kbe\tools\server\pycluster\cluster_controller.py" shutdown %uid%)

pause