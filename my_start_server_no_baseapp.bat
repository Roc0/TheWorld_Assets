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

rd /S /Q %curpath%\logs

@rem  --hide=1
cmdow "KBE machine KBE">nul 2>&1
if %errorlevel%==1 start "KBE machine KBE" "%KBE_BIN_PATH%/machine.exe" --cid=1000 --gus=1
cmdow "KBE logger KBE">nul 2>&1
if %errorlevel%==1 start "KBE logger KBE" "%KBE_BIN_PATH%/logger.exe" --cid=2000 --gus=2
cmdow "KBE interfaces KBE">nul 2>&1
if %errorlevel%==1 start "KBE interfaces KBE" "%KBE_BIN_PATH%/interfaces.exe" --cid=3000 --gus=3
cmdow "KBE dbmgr KBE">nul 2>&1
if %errorlevel%==1 start "KBE dbmgr KBE" "%KBE_BIN_PATH%/dbmgr.exe" --cid=4000 --gus=4
cmdow "KBE baseappmgr KBE">nul 2>&1
if %errorlevel%==1 start "KBE baseappmgr KBE" "%KBE_BIN_PATH%/baseappmgr.exe" --cid=5000 --gus=5
cmdow "KBE cellappmgr KBE">nul 2>&1
if %errorlevel%==1 start "KBE cellappmgr KBE" "%KBE_BIN_PATH%/cellappmgr.exe" --cid=6000 --gus=6
cmdow "KBE baseapp KBE">nul 2>&1
rem if %errorlevel%==1 start "KBE baseapp KBE" "%KBE_BIN_PATH%/baseapp.exe" --cid=7001 --gus=7
@rem cmdow "KBE baseapp1 KBE">nul 2>&1
@rem if %errorlevel%==1 start "KBE baseapp1 KBE" "%KBE_BIN_PATH%/baseapp.exe" --cid=7002 --gus=8
cmdow "KBE cellapp KBE">nul 2>&1
if %errorlevel%==1 start "KBE cellapp KBE" "%KBE_BIN_PATH%/cellapp.exe" --cid=8001 --gus=9
@rem cmdow "KBE cellapp1 KBE">nul 2>&1
@rem if %errorlevel%==1 start "KBE cellapp1 KBE" "%KBE_BIN_PATH%/cellapp.exe" --cid=8002  --gus=10
cmdow "KBE loginapp KBE">nul 2>&1
if %errorlevel%==1 start "KBE loginapp KBE" "%KBE_BIN_PATH%/loginapp.exe" --cid=9000 --gus=11

@rem cmdow "KBE bots KBE">nul 2>&1
@rem if %errorlevel%==1 start "KBE bots KBE" "%KBE_BIN_PATH%/bots.exe"

set ROW1_POS=10
set ROW2_POS=353
set ROW3_POS=695

set COL0_POS=0
set COL1_POS=380
set COL2_POS=891
set COL3_POS=1400

rem ROW 1
cmdow.exe "KBE bots KBE" /mov %COL0_POS% %ROW1_POS% /SIZ 390 338
cmdow.exe "KBE logger KBE" /mov %COL1_POS% %ROW1_POS% /SIZ 515 338
cmdow.exe "KBE interfaces KBE" /mov %COL2_POS% %ROW1_POS% /SIZ 515 338
cmdow.exe "KBE loginapp KBE" /mov %COL3_POS% %ROW1_POS% /SIZ 515 338

rem ROW 2
cmdow.exe "KBE baseapp1 KBE" /mov %COL0_POS% %ROW2_POS% /SIZ 390 338
cmdow.exe "KBE baseapp KBE" /mov %COL1_POS% %ROW2_POS% /SIZ 515 338
cmdow.exe "KBE baseappmgr KBE" /mov %COL2_POS% %ROW2_POS% /SIZ 515 338
cmdow.exe "KBE dbmgr KBE" /mov %COL3_POS% %ROW2_POS% /SIZ 515 338

rem ROW 3
cmdow.exe "KBE cellapp1 KBE" /mov %COL0_POS% %ROW3_POS% /SIZ 390 338
cmdow.exe "KBE cellapp KBE" /mov %COL1_POS% %ROW3_POS% /SIZ 515 338
cmdow.exe "KBE cellappmgr KBE" /mov %COL2_POS% %ROW3_POS% /SIZ 515 338
cmdow.exe "KBE machine KBE" /mov %COL3_POS% %ROW3_POS% /SIZ 515 338

