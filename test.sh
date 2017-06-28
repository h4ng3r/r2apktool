#!/bin/bash

wget https://github.com/radare/radare2-regressions/blob/master/bins/dex/Hello.apk?raw=true --quiet -O Hello.apk

python r2apktool.py Hello.apk

wget https://github.com/radare/radare2-regressions/blob/master/bins/dex/org.radare.radare2installer.apk?raw=true