import sys
from cx_Freeze import setup, Executable

exe = Executable(
	script="Pauk.py",
	base="Win32Gui",
	icon="Icon.ico",
	 )

includefiles=["keywords_militar.txt","setup\msvcr100.dll","Icon.ico","spider_move.gif","spider_move2.gif"]
includes=[]
excludes=[]
packages=[]
	 
setup( 
	name = "Паук",
	version = "3.3",
	description = "New gathering",
	options = {"build_exe": {"packages": packages, "excludes": [],'include_files':includefiles}},
	executables = [exe]
	)
