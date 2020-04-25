#!/usr/bin/env bash

cp h2serverconfig.ini.template h2serverconfig.ini
sed -e "s/\${1}/$1/" -e "s/\${2}/$2/" -e "s/\${3}/$3/" -e "s/\${4}/$4/" -e "s/\${5}/$5/" -e "s/\${6}/$6/" -e "s/\${7}/$7/" -e "s/\${8}/$8/" -e "s/\${9}/$9/" -e "s/\${10}/$10/" -e "s/\${11}/$11/" h2serverconfig.ini