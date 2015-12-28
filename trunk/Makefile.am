## Process this file with automake to produce Makefile.in
## Created by Anjuta

SUBDIRS = src 

eyeguard_pydocdir = ${prefix}/doc/eyeguard_py
eyeguard_pydoc_DATA = \
	README\
	COPYING\
	AUTHORS\
	ChangeLog\
	INSTALL\
	NEWS


EXTRA_DIST = $(eyeguard_pydoc_DATA)


# Remove doc directory on uninstall
uninstall-local:
	-rm -r $(eyeguard_pydocdir)
