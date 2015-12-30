import sys
from cx_Freeze import setup, Executable

exe = Executable(
     script="Pauk.py",
     base="Win32Gui"
     )

includefiles=["keywords_militar.txt","setup\history.txt","setup\msvcr100.dll","Icon.ico"]
includes=[]
excludes=[]
packages=[]
	 
setup( 
	name = "Pauk",
	version = "3.3",
	description = "New gathering",
	options = {"build_exe": {"packages": packages, "excludes": [],'include_files':includefiles}},
	executables = [exe]
	)
