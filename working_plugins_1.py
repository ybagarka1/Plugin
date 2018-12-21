#!/cygdrive/c/Users/yash.bagarka/AppData/Local/Programs/Python/Python36/python
config_file ={"config": {"agentcoreversion": "dev_platform-agent-core","performanceversion": "dev_platform-performance-plugin"}}

import os
import requests
import json
import yaml
import sys
from artifactory import ArtifactoryPath

## required variables
#artifactory_url = 'http://artifact.corp.continuum.net:8081'
artifactory_url = os.environ['artifactory_url']
#repo_name = ['dt-dev_its-portal-net','dt_dev_yash']
repo_name = os.environ['repo_name']
# artifactory user name
artifactory_username = 'repluser'
# artifactoy password
artifactory_password = os.environ['artifactory_password']
aql = ArtifactoryPath("{}/artifactory/".format(artifactory_url), auth=('{}'.format(artifactory_username),'{}'.format(artifactory_password)))
f = open("manifest_source_file", 'w')
header = { 'username': 'repluser', 'password': 'AP49A5SMDpZuQb7e9g7Tn5c45fbUfJkZMzmUSM', 'Content-Type' : 'application/json' }

class artifact:
  def __init__(self,repo_name):
    self.repo_name = repo_name
  def artifactory_version_call(self):
    print(self.repo_name)
    released_builds = aql.aql("builds.find", {"name":{"$match": "{}".format(self.repo_name)},"promotion.status": {"$eq":"Released"}},".sort",({"$desc":["number"]}))
    latest_released_build = released_builds[0]["build.number"]
    return latest_released_build

'''
class artifact:
  def __init__(self,repo_name):
    self.repo_name = repo_name
  def artifactory_version_call(self): 
    response = requests.get("http://artifact.corp.continuum.net:8081/artifactory/{0}".format(self.repo_name), data=header)
    soup = BeautifulSoup(response.content, "html.parser")
    b = soup.find_all("a")
    data = []
    builds = []
    buildno = []
    for tag in b:
      data=tag.attrs['href']
      builds = tag.attrs['href'].replace("/", "")
      buildno.append(int(builds))
    latest_version = max(buildno)
    return latest_version
'''
plugins_info = open('plugins_info.yml')  
plugins = yaml.safe_load(plugins_info)
plugins_info.close()
for i in config_file['config']:
  try:
    if os.environ[i] in config_file:
      print("Value is not defined")
  except KeyError:	
    print("Val for " + i + " not defined.Need to get the latest version from artifactory using repo name:" + config_file['config'][i])
    repo_name = config_file['config'][i]
    ## get request to artifactory to get the version
    artifact_call = artifact(repo_name)
    version = artifact_call.artifactory_version_call()
    print(version)
    f.write("export " + i + "=" + str(version) +"\n")
  else:
    f.write("export " + i + "=" + os.environ[i] + "\n")
