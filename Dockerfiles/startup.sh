#!/usr/bin/env bash

# Set the approriate registry settings
wine regedit h2server.reg

# Verify registry was set
wine regedit /E output.reg "HKEY_CURRENT_USER\Software\Microsoft\Halo 2\Server\LIVE"
cat output.reg

# Install the service
wine /home/h2server/h2server.exe -createservice -live -instance:1 || true
wine /home/h2server/h2server.exe -service -live -h2config=/home/config/h2serverconfig.ini