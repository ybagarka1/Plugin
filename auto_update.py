#!/cygdrive/c/Users/yash.bagarka/AppData/Local/Programs/Python/Python36/python
## Author: Yash Bagarka ##
## version: v1 ##
config_file ={"config": {"agentcoreversion": "dev_platform-agent-core","performanceversion": "dev_platform-performance-plugin"}}

import os
import requests
import json
import yaml
import sys
from artifactory import ArtifactoryPath
from requests.auth import HTTPBasicAuth

## required variables
#artifactory_url = 'http://artifact.corp.continuum.net:8081'
artifactory_url = os.environ['artifactory_url']
#repo_name = ['dt-dev_its-portal-net','dt_dev_yash']
#repo_name = os.environ['repo_name']
# artifactory user name
artifactory_username = 'repluser'
# artifactoy password
artifactory_password = os.environ['artifactory_password']
aql = ArtifactoryPath("{}/artifactory/".format(artifactory_url), auth=('{}'.format(artifactory_username),'{}'.format(artifactory_password)))
f = open("manifest_source_file", 'w')

global_manifest = {}
global_manifest['packages'] = []


class artifactory_aql_call:
  def __init__(self,repo_name,release_env):
    self.repo_name = repo_name
    self.release_env = release_env
  def artifactory_version_call(self):
    released_builds = aql.aql("builds.find", {"name":{"$match": "dev_{}".format(self.repo_name)},"promotion.status": {"$eq":"{}".format(self.release_env)}},".sort",({"$desc":["number"]}))
    all_builds_no = []
    for i in released_builds:
        all_builds_no.append(int(i["build.number"]))
    max_build_no = max(all_builds_no) 
    build_info = requests.get("{}/artifactory/api/build/dev_{}/{}".format(artifactory_url,repo_name,max_build_no), auth=HTTPBasicAuth(artifactory_username,artifactory_password))
    build_info_json = json.loads(build_info.text)
    for i in build_info_json["buildInfo"]["modules"][0]["artifacts"]:
        if str(32) in i["name"]:
            version_value = i["name"].rsplit('_',1)[1].rsplit('.zip',1)[0]
    return version_value  

class latest_build:
    def __init__(self,repo_name):
        self.repo_name = repo_name
    def artifactory_call(self):
        promotion_status = 'Released, PROD Ready, Stage Ready, QA Ready, DT_Ready'
        for i in promotion_status.split(','):
            latest_build_call = artifactory_aql_call(self.repo_name, i)
            latest_build_value = latest_build_call.artifactory_version_call()
            if latest_build_value is not None:
                break
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
        print("The build number for repo "+i["repo_name"]+" is not passed...the lastest released value is "+str(version))
        print("Creating global manifest file")
        global_manifest['packages'].append({ "name": "{}".format(repo_name), "type": "{}".format(i["type"]), "version": "{}".format(version), "sourceURL": "{{ downloadurl }}/Windows/{}/{}/{}".format(repo_name, version,version)})

with open('globalmanifest.json', 'w') as outfile:
    json.dump(global_manifest, outfile)

'''
        f.write("export " + i + "=" + str(version) +"\n")
    else:
        f.write("export " + i + "=" + os.environ[i] + "\n")
'''
