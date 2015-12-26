import sys
from cx_Freeze import setup, Executable

exe = Executable(
     script="Pauk.py",
     base="Win32Gui"
     )

includefiles=["keywords_militar.txt","setup\history.txt","setup\msvcr100.dll"]
includes=[]
excludes=[]
packages=[]
	 
setup( 
	name = "Паук", 
	version = "1.0", 
	description = "Сбор новостей по ключевым словам",
	options = {"build_exe": {"packages": packages, "excludes": [],'include_files':includefiles}},
	executables = [exe]
	)
