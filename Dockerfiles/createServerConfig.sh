#!/usr/bin/env bash

cp h2serverconfig.ini.template h2serverconfig.ini
sed -e "s/\${1}/$1/" -e "s/\${2}/$2/" h2serverconfig.ini