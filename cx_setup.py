#!/usr/bin/env python

error = ""

import os, sys, struct
from distutils import log, dir_util, sysconfig
try:
	from cx_Freeze import setup, Executable 
except ImportError:
	error += "ImportError: cx_Freeze not found (http://cx-freeze.sourceforge.net/)\n"

if error:
	sys.exit(error)

def split_path(path):

	folders = []

	while True:
		path, base = os.path.split(path)

		if base != "":
			folders.append(base)
		# base is entire path and cannot be split
		else:
			if path != "":
				folders.append(path)

			break

	folders.reverse()

	return folders

base = None
base_gui = None
if sys.platform == "win32":
	base_gui = "Win32GUI"

data = []
for d, subdirs, files in os.walk(os.path.join("lass","data")):
	for f in files:
		out = os.path.join(*(split_path(d)[1:] + [f]))
		data.append((os.path.join(d,f), out))

for d, subdirs, files in os.walk("lib"):
	for f in files:
		out = os.path.join("data", "lua", "5.1", *(split_path(d)[1:] + [f]))
		data.append((os.path.join(d,f), out))

setup(
	name = "lass",
	version = "0.1.0.dev0",
	author = "Decky Coss",
	author_email = "coss@cosstropolis.com",
	description = "A modular development kit for 2D videogames.",
	# packages = ["lass", "lass.gui", "lass.gui.ui"],
	# install_requires = ["jinja2", "lupa", "six", "PySide"],
	executables = [
		Executable(os.path.join("bin", "lasspm"), base=base),
		Executable(os.path.join("bin", "lass"), base=base_gui)
	],
	options = {
		"build_exe":{
			"include_files":data,
			"packages": ["lass", "lass.gui", "lass.gui.ui", "jinja2", "lupa", "six", "PySide"]
		}
	}
)
