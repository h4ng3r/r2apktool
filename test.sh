#!/bin/bash

echo "Testing Hello.apk"

wget https://github.com/radare/radare2-regressions/blob/master/bins/dex/Hello.apk?raw=true --quiet -O Hello.apk

python r2apktool.py -f Hello.apk

diff tests/Hello.apk_Hello.smali Hello/Hello.smali 

#echo "Testing r2installer.apk"

#wget https://github.com/radare/radare2-regressions/blob/master/bins/dex/org.radare.radare2installer.apk?raw=true --quiet -O org.radare.radare2installer.apk

#python r2apktool.py -f org.radare.radare2installer.apk


