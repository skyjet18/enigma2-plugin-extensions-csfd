#!/bin/bash

for lang in cs sk ; do
	# extract clean list of strings
	xgettext -L python ../*.py --no-location --no-wrap --foreign-user --package-name=enigma2-plugin-extension-csfd --package-version='' --copyright-holder='' -o ${lang}.pot

	# mark obsolete strings
	msgattrib --set-obsolete --ignore-file=${lang}.pot -o ../locale/$lang/LC_MESSAGES/CSFD.po ../locale/$lang/LC_MESSAGES/CSFD.po
	
	# remove obsolete strings
	msgattrib --no-obsolete -o ../locale/$lang/LC_MESSAGES/CSFD.po ../locale/$lang/LC_MESSAGES/CSFD.po
	
	# remove clean strings file
	rm ${lang}.pot
	
	# add new strings
	xgettext -L python ../*.py --no-location --no-wrap --foreign-user --package-name=enigma2-plugin-extension-csfd --package-version='' --copyright-holder='' -j -o ../locale/$lang/LC_MESSAGES/CSFD.po
done
