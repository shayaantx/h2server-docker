#!/usr/bin/env bash
cp h2server.reg.template h2server.reg
sed -e "s/\${1}/$1/" -e "s/\${2}/$2/" h2server.reg