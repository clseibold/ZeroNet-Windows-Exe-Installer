@echo off
cd %~dp0

python --version>NUL
if errorlevel 1 goto NoPython

rem. If py exists, use it to run python2, else just use python
py>NUL
if errorlevel 1 goto UsePython

:UsePy
if "%1" == "" (
	py -2 -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet start.py
) else (
	if not exist ZeroNet (
		py -2 -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet zeronet.py %*
	) else (
		cd ZeroNet
		py -2 zeronet.py %*
		cd ..
	)
)

:UsePython
if "%1" == "" (
	python -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet start.py
) else (
	if not exist ZeroNet (
		python -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet zeronet.py %*
	) else (
		cd ZeroNet
		python zeronet.py %*
		cd ..
	)
)

:NoPython
echo You must have Python 2 installed and in Path to start ZeroNet.