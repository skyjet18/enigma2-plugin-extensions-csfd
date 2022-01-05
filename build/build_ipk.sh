#!/bin/bash

if [ "$1" = "" ] ; then
	echo "Usage: $0 version"
	exit 1
fi

DATE=`date +%d.%m.%Y`
VER=${1}

if [ -z `echo $VER | grep '^[[:digit:]][[:digit:]]\.[[:digit:]][[:digit:]]$'` ] ; then
	echo "Version in wrong format - must be xx.yy eg. 13.10"
	exit 1
fi

VER_WITH_DATE=${1}-`date +%Y%m%d`
VER_WITH_DATE2=$(echo $VER_WITH_DATE | tr '.' '-')

E_VER=$(printf '%s\n' "$VER" | sed -e 's/[\/&]/\\&/g')
E_VER_WITH_DATE=$(printf '%s\n' "$VER_WITH_DATE2" | sed -e 's/[\/&]/\\&/g')
E_DATE=$(printf '%s\n' "$DATE" | sed -e 's/[\/&]/\\&/g')

PKG_NAME=enigma2-plugin-extensions-csfd_${VER_WITH_DATE2}_all.ipk
E_PKG_NAME=$(printf '%s\n' "$PKG_NAME" | sed -e 's/[\/&]/\\&/g')

sed -i "s/Version:\ .*/Version:\ $E_VER_WITH_DATE/" control/control
sed -i "s/CSFDVersion=.*/CSFDVersion=\'${E_VER}\'/" ../CSFDSettings2.py
sed -i "s/CSFDVersionData=.*/CSFDVersionData=\'${E_DATE}\'/" ../CSFDSettings2.py
sed -i "1s/.*/$E_VER/" ../version.txt
sed -i "1s/.*/$E_VER/" ../versionbeta.txt
sed -i "2s/.*/$E_PKG_NAME/" ../version.txt
sed -i "2s/.*/$E_PKG_NAME/" ../versionbeta.txt
sed -i "s/Version:\ [[:digit:]][[:digit:]]\.[[:digit:]][[:digit:]]/Version:\ $E_VER/" ../maintainer.info

CUR_DIR=`pwd`

pushd control/
tar --numeric-owner --group=0 --owner=0 -czf $CUR_DIR/control.tar.gz ./*
popd

pushd ..
tar --transform 's,^,usr/lib/enigma2/python/Plugins/Extensions/CSFD/,' --exclude-vcs --exclude-vcs-ignore --exclude=build --exclude=logs --numeric-owner --group=0 --owner=0 -czf $CUR_DIR/data.tar.gz ./*
popd

echo "2.0" > $CUR_DIR/debian-binary
ar rv ${CUR_DIR}/${PKG_NAME} $CUR_DIR/debian-binary $CUR_DIR/control.tar.gz $CUR_DIR/data.tar.gz

rm $CUR_DIR/debian-binary
rm $CUR_DIR/control.tar.gz
rm $CUR_DIR/data.tar.gz
cp $PKG_NAME `basename -s .ipk $PKG_NAME`.deb
