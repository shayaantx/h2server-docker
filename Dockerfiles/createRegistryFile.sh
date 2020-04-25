#!/usr/bin/env bash
cp h2server.reg.template
sed -e "s/\${1}/$1/" -e "s/\${2}/$2/" h2server.reg.template | tee h2server.reg