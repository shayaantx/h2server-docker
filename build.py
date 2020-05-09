import yaml
import os
import re

###########
# Globals #
###########

h2ServerConfigKeys = {}
h2ServerInstanceIds = []
h2ServerInstancePattern = re.compile("H2SERVER([0-9]+)")


# We have a special class for KeyValue types where we want double quotes surrounding the key AND value
# docker-compose doesn't seem to treat double quotes on the key AND value separately as valid
class BaseKeyValueType:
  def __init__(self, key, value):
    self.key = key
    self.value = value


class BuildArgsKeyValueType(BaseKeyValueType):
  pass


class PortKeyValueType(BaseKeyValueType):
  pass


class VolumeKeyValueType(BaseKeyValueType):
  pass


def doubleQuoteAroundKeyAndValueRepresenter(dumper, data):
  newKeyValue = data.key + ':' + data.value
  return dumper.represent_scalar('tag:yaml.org,2002:str', newKeyValue, style='"')


def buildArgsKeyValueTypeRepresenter(dumper, data):
  newKeyValue = data.key + ':"' + data.value + "\""
  return dumper.represent_scalar('tag:yaml.org,2002:str', newKeyValue, style='')


def generalStrKeyValueRepresenter(dumper, data):
  return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


yaml.add_representer(str, generalStrKeyValueRepresenter)
yaml.add_representer(PortKeyValueType, doubleQuoteAroundKeyAndValueRepresenter)
yaml.add_representer(VolumeKeyValueType, doubleQuoteAroundKeyAndValueRepresenter)
yaml.add_representer(BuildArgsKeyValueType, buildArgsKeyValueTypeRepresenter)


def getKeyAndValue(line):
  lineAndValueArr = line.split('=', 1)
  if len(lineAndValueArr) != 2:
    return None, None
  return lineAndValueArr[0], lineAndValueArr[1]


def addLine(line):
  return line + os.linesep


def validateValueAndGetKey(key):
  value = h2ServerConfigKeys.get(key, None)
  if value == None or not value:
    raise ValueError("Could not find " + key + " or value is empty")
  return key


def variablize(value):
  return "${" + value + "}"


def getH2ServerBlock(id):
  h2ServerContainerName = "h2server" + id

  h2ServerUniqueStringPrefix = "H2SERVER" + id + "_"
  h2ServerDescription = validateValueAndGetKey(h2ServerUniqueStringPrefix + "DESCRIPTION")
  h2ServerOwner = validateValueAndGetKey(h2ServerUniqueStringPrefix + "OWNER")
  h2ServerUdpPortRange = validateValueAndGetKey(h2ServerUniqueStringPrefix + "UDP_PORT_RANGE")
  h2ServerTcpPort = validateValueAndGetKey(h2ServerUniqueStringPrefix + "TCP_PORT")
  h2ServerLogsDirectory = validateValueAndGetKey(h2ServerUniqueStringPrefix + "LOGS_DIRECTORY")
  h2ServerEnableXDelay = validateValueAndGetKey(h2ServerUniqueStringPrefix + "ENABLE_XDELAY")
  h2ServerName = validateValueAndGetKey(h2ServerUniqueStringPrefix + "SERVER_NAME")
  h2ServerPlaylist = validateValueAndGetKey(h2ServerUniqueStringPrefix + "SERVER_PLAYLIST")
  h2ServerUsername = validateValueAndGetKey(h2ServerUniqueStringPrefix + "USERNAME")
  h2ServerPassword = validateValueAndGetKey(h2ServerUniqueStringPrefix + "PASSWORD")

  h2ServerArgs = [
    BuildArgsKeyValueType("description", variablize(h2ServerDescription)),
    BuildArgsKeyValueType("owner", variablize(h2ServerOwner)),
    BuildArgsKeyValueType("udp_port_range", variablize(h2ServerUdpPortRange)),
    BuildArgsKeyValueType("tcp_port", variablize(h2ServerTcpPort)),
    BuildArgsKeyValueType("logs_directory", variablize(h2ServerLogsDirectory)),
    BuildArgsKeyValueType("enable_xdelay", variablize(h2ServerEnableXDelay)),
    BuildArgsKeyValueType("server_name", variablize(h2ServerName)),
    BuildArgsKeyValueType("server_playlist", variablize(h2ServerPlaylist)),
    BuildArgsKeyValueType("username", variablize(h2ServerUsername)),
    BuildArgsKeyValueType("password", variablize(h2ServerPassword))
  ]

  h2ServerBuild = {"context": "./Dockerfiles", "dockerfile": "Dockerfile", "args": h2ServerArgs}
  return {
    h2ServerContainerName: {
      "build": h2ServerBuild,
      "ports": [
        PortKeyValueType(variablize(h2ServerUdpPortRange), variablize(h2ServerUdpPortRange) + "/udp"),
        PortKeyValueType(variablize(h2ServerTcpPort), variablize(h2ServerTcpPort) + "/tcp")
      ],
      "volumes": [VolumeKeyValueType(variablize(h2ServerLogsDirectory),
                                   "/root/.wine/drive_c/users/root/Local Settings/Application Data/Microsoft/Halo 2/logs/H2Server/instance1")],
      "extends": {"file": "docker-common.yml", "service": "h2server"}
    }
  }


###############
# Main Script #
###############

# read all the lines in the .env file
with open(".env") as file:
  environmentLines = file.readlines()

# populate key map with all the configuration
for line in environmentLines:
  # Turn on for troubleshooting
  # print(line)
  if line.startswith("#"):
    continue
  key, value = getKeyAndValue(line)
  if key != None:
    h2ServerConfigKeys[key] = value
    h2ServerInstanceIdMatchResult = h2ServerInstancePattern.search(key)
    if h2ServerInstanceIdMatchResult != None:
      h2ServerInstanceId = h2ServerInstanceIdMatchResult.group(1)
      if h2ServerInstanceId not in h2ServerInstanceIds:
        h2ServerInstanceIds.append(h2ServerInstanceId)

if not h2ServerInstanceIds:
  raise ValueError("No h2 server instances configured")

h2ServerDictionary = dict()
h2ServerDictionary.update({"version": "2"})

h2ServersDict = dict()
for h2ServerInstance in h2ServerInstanceIds:
  h2ServersDict.update(getH2ServerBlock(h2ServerInstance))

h2ServerDictionary.update({"services": h2ServersDict})

# write the yaml file out to disk
with open(r'docker-compose.yml', 'w') as file:
  documents = yaml.dump(h2ServerDictionary, file, default_style=None, default_flow_style=False)
