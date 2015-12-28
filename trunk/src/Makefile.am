## Process this file with automake to produce Makefile.in
## Created by Anjuta



## The main script
bin_SCRIPTS = eyeguard_py.py \
	EgSetting.py \
	EgLockScreen.py

## Directory where .class files will be installed
eyeguard_pydir = $(pythondir)/eyeguard_py


eyeguard_py_PYTHON = \
	eyeguard_py.py



# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(pkgdatadir)
