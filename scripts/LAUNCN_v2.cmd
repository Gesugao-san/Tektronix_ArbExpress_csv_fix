
@ECHO OFF
CLS

python --version 3 1>nul 2>nul

IF ERRORLEVEL 1 GOTO errorNoPython
GOTO start

:errorNoPython
ECHO.
ECHO FATAL ERROR^: Python 3 is not installed. Please install from:
ECHO.
ECHO.  http://python.org
ECHO.
PAUSE
GOTO :EOF

:start
CD /D "..\src\"
@ECHO ON
py ".\main.py" --full_mode 1
@ECHO OFF
PAUSE
