#!/usr/bin/env bash

# Set the approriate registry settings
wine regedit h2server.reg

# Verify registry was set
wine regedit /E output.reg "HKEY_CURRENT_USER\Software\Microsoft\Halo 2\Server\LIVE"
cat output.reg

# h2server has an interactive shell that doesn't work well with docker-compose, so we wrap this logic in a screen session instead
# you can use h2server with docker run, but the point of this setup is to run many servers via docker-compose
screen -d -m wine /home/h2server/h2server.exe -live -h2config=/home/config/h2serverconfig.ini

if pgrep -x h2server.exe >/dev/null
then
  # if for any reason the serve stops, stop this entrypoint
  echo "service is not running"
  exit 1
else
  sleep 10
fi