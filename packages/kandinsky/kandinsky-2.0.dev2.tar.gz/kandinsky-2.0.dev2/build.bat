@echo off

copy /y src\kandinsky\README.md .\
rd /s /q .\dist
python .\config.py
python -m build
pause