@echo off
cd %~dp0
if not exist ZeroNet (
	Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet zeronet.py %*
) else (
	Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet update.py
)