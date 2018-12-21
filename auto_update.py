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


class artifactory_aql_call:
  def __init__(self,repo_name,release_env):
    self.repo_name = repo_name
    self.release_env = release_env
  def artifactory_version_call(self):
    released_builds = aql.aql("builds.find", {"name":{"$match": "dev_{}".format(self.repo_name)},"promotion.status": {"$eq":"{}".format(self.release_env)}},".sort",({"$desc":["number"]}))
    latest_released_build_info = released_builds[0]["build.number"]
    return latest_released_build_info

class latest_build:
    def __init__(self,repo_name):
        self.repo_name = repo_name
    def artifactory_call(self):
        promotion_status = "Released, PROD Ready, Stage Ready,QA Ready, DT-Ready"
        for i in promotion_status.split(','):
            latest_build_call = artifactory_aql_call(self.repo_name, i)
            latest_build_value = latest_build_call.artifactory_version_call()
            if latest_build_value is not None:
                break;
        return latest_build_value

plugins_info = open('plugins_info.yml')  
plugins = yaml.safe_load(plugins_info)
plugins_info.close()

for i in plugins['plugins']:
    value = i["name"]
    try:
        os.environ[value]
        print("The build number for repo "+i["repo_name"]+" is "+os.environ[value])
    except KeyError:
        repo_name = i["repo_name"]
        ## get request to artifactory to get the version
        artifact_call = latest_build(repo_name)
        version = artifact_call.artifactory_call()
        print("The build number for repo "+i["repo_name"]+" is not passed...the lastest released value is "+version)
'''
        f.write("export " + i + "=" + str(version) +"\n")
    else:
        f.write("export " + i + "=" + os.environ[i] + "\n")
'''
