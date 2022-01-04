#!/bin/bash

if [ "$1" = "" ] ; then
	echo "Usage: $0 version"
	exit 1
fi

DATE=`date +%d.%m.%Y`
VER=${1}-`date +%Y%m%d`
VER2=$(echo $VER | tr '.' '-')
VER3=${1}

ESCAPED_VER3=$(printf '%s\n' "$VER3" | sed -e 's/[\/&]/\\&/g')
ESCAPED_VER2=$(printf '%s\n' "$VER2" | sed -e 's/[\/&]/\\&/g')
ESCAPED_DATE=$(printf '%s\n' "$DATE" | sed -e 's/[\/&]/\\&/g')

sed -i "2s/.*/Version:\ $ESCAPED_VER2/" control/control
sed -i "s/CSFDVersion=.*/CSFDVersion=\'${ESCAPED_VER3}\'/" ../CSFDSettings2.py
sed -i "s/CSFDVersionData=.*/CSFDVersionData=\'${ESCAPED_DATE}\'/" ../CSFDSettings2.py

PKG_NAME=enigma2-plugin-extensions-csfd_${VER2}_all.ipk
CUR_DIR=`pwd`

pushd control/
tar --numeric-owner --group=0 --owner=0 -czf $CUR_DIR/control.tar.gz ./*
popd

pushd ..
tar --transform 's,^,usr/lib/enigma2/python/Plugins/Extensions/CSFD/,' --exclude-vcs --exclude-vcs-ignore --exclude=build --exclude=logs --numeric-owner --group=0 --owner=0 -czf $CUR_DIR/data.tar.gz ./*
popd

echo "2.0" > $CUR_DIR/debian-binary
# tar --numeric-owner --group=0 --owner=0 -cf ${CUR_DIR}/${PKG_NAME} $CUR_DIR/debian-binary $CUR_DIR/data.tar.gz $CUR_DIR/control.tar.gz
ar rv ${CUR_DIR}/${PKG_NAME} $CUR_DIR/debian-binary $CUR_DIR/data.tar.gz $CUR_DIR/control.tar.gz

rm $CUR_DIR/debian-binary
rm $CUR_DIR/control.tar.gz
rm $CUR_DIR/data.tar.gz
