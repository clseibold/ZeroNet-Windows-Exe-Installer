@echo off
cd %~dp0

python --version>NUL
if errorlevel 1 goto NoPython

rem. If py exists, use it to run python2, else just use python
py>NUL
if errorlevel 1 goto UsePython

:UsePy
if "%1" == "" (
	cd ZeroNet
	py -2 start.py
	cd ..
) else (
	cd ZeroNet
	py -2 zeronet.py %*
	cd ..
)
goto end

:UsePython
if "%1" == "" (
	cd ZeroNet
	python start.py
	cd ..
) else (
	cd ZeroNet
	python zeronet.py %*
	cd ..
)
goto end

:NoPython
echo You must have Python 2 installed and in Path to start ZeroNet.

:end
pause