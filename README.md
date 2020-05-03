# Summary

This set of docker configurations enables someone to host halo2vista dedicated (h2server) in docker via wine.
 - h2server.exe is typically run on windows as a service
 - We have found through testing that h2server.exe can run on wine just fine with no performance drops

## Prerequisites 

- Familarity using docker and docker-compose
- Ability to open ports
- Ability to linux based distributions
- Ability to use git

## Setup

1. Clone the git repo
1. Edit the .env file (all the h2server properties live in this file)
    * The environment file consists of global variables and server specific variables
    * All the global variables are required (see .env file for explanations of variables)
      * H2SERVER_PLAYLISTS_DIRECTORY
      * H2SERVER_BINARIES
      * H2SERVER_WAN_IP 
      * H2SERVER_LAN_IP
      * H2SERVER_DEBUG_LOG
      * H2SERVER_DEBUG_LOG_LEVEL
      * H2SERVER_DEBUG_LOG_CONSOLE
      * H2SERVER_PCR_TIME
    * The individual server config variables are all named H2SERVER<number>_<property-name>
    * For example: H2SERVER1_UDP_PORT_RANGE, H2SERVER2_OWNER, etc (see the .env file for the list of these variables)
    * All variables should be set
1. You have two options at this point: manually configure docker-compose.yml or use build.sh (which builds the yml from the .env file)

* ### Manual
  1. Copy the docker-compose.yml.sample file and rename to docker-compose.yml
  1. By default only one server exists in the sample, if you want to add another h2server, add another block under "services:"
  ```yaml
  services:
    h2server1:
      build:
        context: ./Dockerfiles
        dockerfile: Dockerfile
        args:
          description: "${H2SERVER1_DESCRIPTION}"
      ...
    h2server2:
      build:
        context: ./Dockerfiles
        dockerfile: Dockerfile
        args:
          description: "${H2SERVER2_DESCRIPTION}"
      ...
  ```
  1. 
* ### Automated
  1. TODO

## Usage

TODO: docker-compose

## Other

If you don't want to use docker-compose, running the the default wine container with below syntax works just as well

* Syntax (replace each <> placeholder)

```sh
docker run -p <udp-port-range>:<udp-port-range>/udp -p <tcp-port>:<tcp-port>/tcp -v "<host-location-of-h2server-playlists>:/home/wineuser/.wine/drive_c/users/wineuser/My Documents/My Games/Halo 2/Server" -v <host-location-of-h2server-binaries>:/home/h2server -v <host-location-of-h2server-config-ini>:/home/h2serverconfig1.ini -it scottyhardy/docker-wine wine /home/h2server/h2server.exe -live -h2config=/home/h2serverconfig1.ini
```

* Example

```sh
docker run -p 50000-50009:50000-50009/udp -p 50010:50010/tcp -v "/root/h2server-binaries/playlists:/home/wineuser/.wine/drive_c/users/wineuser/My Documents/My Games/Halo 2/Server" -v /root/h2server-binaries:/home/h2server -v /root/h2serverconfig1.ini:/home/h2serverconfig1.ini -it scottyhardy/docker-wine wine /home/h2server/h2server.exe -live -h2config=/home/h2serverconfig1.ini
```
