SET folder=%~dp0
cd %folder%
call C:\ProgramData\Anaconda3\Scripts\activate.bat
call C:\Users\%USERNAME%\AppData\Local\Continuum\Anaconda3\Scripts\activate.bat
call activate defaultVenv
call set PATH=%PATH%;C:\MinGW\bin
cd \
python -V
call python "%folder%main.py"
cmd /k 