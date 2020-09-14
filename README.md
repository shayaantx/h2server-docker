# Summary

This set of docker configurations enables someone to host halo2vista dedicated (h2server) in docker via wine.
 - h2server.exe is typically run on windows as a service
 - We have found through testing that h2server.exe can run on wine just fine with no performance drops

## Prerequisites 

- Familarity using docker and docker-compose
- Ability to open ports
- Ability to use linux based distributions
- Ability to use git
- Make sure following is installed:
    - git
    - docker
    - docker-compose
    - python
    - python-yaml

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

* ### Automated
  1. Unless you are used to docker, the yaml configuration might be overwhelming, so I made a shell/python script that reads the .env file and builds it for you
  2. Make sure you have python installed and the following packages available in your python install: yaml, os, re
  3. In the git workspace run ./build.sh
  4. This will produce docker-compose.yml
  5. You can run docker-compose config in the git workspace to validate the config is valid.
  6. Every time you change the .env file, make sure to run ./build.sh to rebuild the file

## Usage

1. I've made a few scripts to assist users with starting and stopping containers (for the less docker friendly people)
    * restart.sh
    * stop.sh
1. Both of these scripts basically call docker-compose up or docker-compose down
1. If you want to connect to administer your h2server, follow below steps
    1. docker ps
    1. Get the container id
    1. docker exec -it <container-id> screen -r
    1. Don't ctrl+c or type exit, since that will exit the server, always end with Ctrl+a+d (we are running screen here due to some interactive shell annoyance with h2server.exe -live mode)    

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
