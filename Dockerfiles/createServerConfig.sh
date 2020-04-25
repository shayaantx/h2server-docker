#!/usr/bin/env bash
# arguments for this shell script over 9 use ${N} syntax
sed -e "s/\${var1}/$1/" -e "s/\${var2}/$2/" -e "s/\${var3}/$3/" -e "s/\${var4}/$4/" -e "s/\${var5}/$5/" -e "s/\${var6}/$6/" -e "s/\${var7}/$7/" -e "s/\${var8}/$8/" -e "s/\${var9}/$9/" -e "s/\${var10}/${10}/" -e "s/\${var11}/${11}/" h2serverconfig.ini.template | tee h2serverconfig.ini