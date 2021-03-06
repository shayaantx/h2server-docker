FROM scottyhardy/docker-wine

RUN apt-get update
RUN apt-get install screen

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

# Build h2server config file
ADD createServerConfig.sh .
ADD h2serverconfig.ini.template .
RUN chmod 755 createServerConfig.sh
RUN ./createServerConfig.sh "$wan_ip" "$lan_ip" "$enable_xdelay" "$debug_log" "$debug_log_level" "$debug_log_console" "$server_name" "$server_playlist" "$pcr_time" "$username" "$password" "$udp_port_range"
RUN mkdir /home/config
RUN mv h2serverconfig.ini /home/config/

ADD startup.sh .
RUN chmod 755 startup.sh

ENTRYPOINT ["./startup.sh"]