FROM scottyhardy/docker-wine

# Make general h2server docker-compose arguments available
ARG wan_ip
ARG lan_ip
ARG debug_log
ARG debug_log_level
ARG debug_log_console
ARG pcr_time

# Make general h2server specific docker-compose arguments available
ARG description
ARG owner
ARG udp_port_range
ARG tcp_port
ARG logs_directory
ARG enable_xdelay
ARG server_name
ARG server_playlist
ARG username
ARG password

# Build h2server registry file
ADD createRegistryFile.sh .
ADD h2server.reg.template .
RUN chmod 755 createRegistryFile.sh
RUN ./createRegistryFile.sh "$description" "$owner"
RUN wine regedit h2server.reg

# Build h2server config file
ADD createServerConfig.sh .
ADD h2serverconfig.ini.template .
RUN chmod 755 createServerConfig.sh
RUN ./createServerConfig.sh "$wan_ip" "$lan_ip" "$enable_xdelay" "$debug_log" "$debug_log_level" "$debug_log_console" "$server_name" "$server_playlist" "$pcr_time" "$username" "$password"
RUN mkdir /home/config
RUN cat h2serverconfig.ini
RUN mv h2serverconfig.ini /home/config/

ENTRYPOINT ["wine", "/home/h2server/h2server.exe", "-live", "-h2config=/home/config/h2serverconfig.ini"]