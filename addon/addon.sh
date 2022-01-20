#!/bin/sh

ADDONPATH=/usr/lib/enigma2/python/Plugins/Extensions/CSFD/addon

if [ -d "/usr/lib/python2.7" ]; then
	echo "python 2.7"
	if [ -f "/usr/lib/python2.7/textwrap.py" ]; then
		echo "textwrap.py OK"
	else
		echo "textwrap.py - kopiruji"
		cp -f $ADDONPATH/textwrap.py /usr/lib/python2.7/textwrap.py
	fi
elif [ -d "/usr/lib/python2.6" ]; then
	echo "python 2.6"
	if [ -f "/usr/lib/python2.6/textwrap.py" ]; then
		echo "textwrap.py OK"
	else
		echo "textwrap.py - kopiruji"
		cp -f $ADDONPATH/textwrap.py /usr/lib/python2.6/textwrap.py
	fi
fi

exit 0
