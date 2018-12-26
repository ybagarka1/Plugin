#!/cygdrive/c/Users/yash.bagarka/AppData/Local/Programs/Python/Python36/python
## Author: Yash Bagarka ##
## version: v1 ##
## Purpose: To create global manifest json file ##
config_file ={"config": {"agentcoreversion": "dev_platform-agent-core","performanceversion": "dev_platform-performance-plugin"}}

import os
import requests
import json
import yaml
import sys
from artifactory import ArtifactoryPath
from requests.auth import HTTPBasicAuth
import re
import pprint

## required variables

#artifactory_url = 'http://artifact.corp.continuum.net:8081'
artifactory_url = os.environ['artifactory_url']
# artifactory user name
artifactory_username = 'repluser'
# artifactoy password
artifactory_password = os.environ['artifactory_password']
aql = ArtifactoryPath("{}/artifactory/".format(artifactory_url), auth=('{}'.format(artifactory_username),'{}'.format(artifactory_password)))

f = open("manifest_source_file", 'w')
global_manifest = {}
global_manifest['packages'] = []

class windows_binary_version:
    def __init__(self, repo_name,max_build_no):
        self.repo_name = repo_name
        self.max_build_no = max_build_no
    def windows_binary_version_artifactory_call(self):
        build_info = requests.get("{}/artifactory/api/build/dev_{}/{}".format(artifactory_url,self.repo_name,self.max_build_no), auth=HTTPBasicAuth(artifactory_username,artifactory_password))
        build_info_json = json.loads(build_info.text)
        try:
            if build_info_json["buildInfo"]["modules"][0]["artifacts"]:
                try:
                    for i in build_info_json["buildInfo"]["modules"][0]["artifacts"]:
                        z = re.search('_windows32_', i["name"])
                        if z:
                            version_value = i["name"].rsplit('_',1)[1].rsplit('.zip',1)[0]
                            return version_value
                            break
                except (KeyError):
                    return self.max_build_no
            else:
                return self.max_build_no
        except KeyError:
            return self.max_build_no


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
    return max_build_no
'''
    build_info = requests.get("{}/artifactory/api/build/dev_{}/{}".format(artifactory_url,repo_name,max_build_no), auth=HTTPBasicAuth(artifactory_username,artifactory_password))
    build_info_json = json.loads(build_info.text)
    for i in build_info_json["buildInfo"]["modules"][0]["artifacts"]:
        if str(32) in i["name"]:
            version_value = i["name"].rsplit('_',1)[1].rsplit('.zip',1)[0]
'''
class latest_build:
    def __init__(self,repo_name):
        self.repo_name = repo_name
    def artifactory_call(self):
        promotion_status = 'Released'
        #PROD Ready, Stage Ready, QA Ready, DT_Ready'
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
        version_call = windows_binary_version(i["repo_name"],os.environ[value])
        try:
            version = version_call.windows_binary_version_artifactory_call() 
            print("repo_name="+i["repo_name"]+" version="+version)
        except TypeError:
            version = os.environ[value]
            print("repo_name="+i["repo_name"]+" version="+version)
        if version != "NA":
            global_manifest['packages'].append({ "name": "{}".format(i["repo_name"]), "type": "{}".format(i["type"]), "version": "{}".format(version), "sourceURL": "{{ downloadurl }}/Windows/{}/{}/{}".format(i["repo_name"], version,version)})
    except KeyError:
        repo_name = i["repo_name"]
        ## get request to artifactory to get the version
        artifact_call = latest_build(repo_name)
        max_build_no = artifact_call.artifactory_call()
        version_call = windows_binary_version(repo_name,max_build_no)
        version = version_call.windows_binary_version_artifactory_call()
        print("The build number for repo "+i["repo_name"]+" is not passed...the lastest released value is "+str(version))
        if version != "NA":
            global_manifest['packages'].append({ "name": "{}".format(repo_name), "type": "{}".format(i["type"]), "version": "{}".format(version), "sourceURL": "{{ downloadurl }}/Windows/{}/{}/{}".format(repo_name, version,version)})

with open('globalmanifest.json', 'w') as outfile:
    json.dump(global_manifest, outfile)
'''
with open('globalmanifest.json', 'r') as f:
    data = f.read()
    global_manifest_json_data = json.loads(data)


pprint.pprint(global_manifest_json_data)

        f.write("export " + i + "=" + str(version) +"\n")
    else:
        f.write("export " + i + "=" + os.environ[i] + "\n")
'''
