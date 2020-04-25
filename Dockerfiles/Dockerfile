FROM scottyhardy/docker-wine

# Build h2server registry file
RUN chmod 755 createRegistryFile.sh
RUN ./createRegistryFile.sh "$description" "$owner"
ADD h2server.reg .
RUN wine regedit h2server.reg

# Build h2server config file
RUN chmod 755 createServerConfig.sh


CMD ["wine", "/home/h2server/h2server.exe", "-live", "-h2config=/home/config/h2serverconfig.ini"]