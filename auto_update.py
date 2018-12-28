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
                        z = re.search('32', i["name"])
                        if z:
                            values = dict()
                            binary_name = i["name"]
                            version_value = i["name"].rsplit('_',1)[1].rsplit('.zip',1)[0]
                            if '.' in version_value:
                                values['version_value'] = version_value
                                values['binary_name'] = binary_name
                                return (values)
                                break
                            elif '.' not in version_value:
                                values['version_value'] = self.max_build_no
                                values['binary_name'] = binary_name
                                return values
                                break
                except (KeyError):
                    print("Cant find 32 bit binary in the build selected for deployment..Ignoring the plugin")
                    version_value = "NA"
                    binary_name = "NA"
                    return (version_value+binary_name)
            else:
                print("the build json doesn't have the artifacts entry in it")
                version_value = "NA"
                binary_name = "NA"
                return  
        except KeyError:
            print("there are some issues in the buildinfosjson returning this plugin value as NA")
            version_value = "NA"
            binary_name = "NA"
            return (version_value, binary_name)


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
            values = version_call.windows_binary_version_artifactory_call()
            version = values["version_value"]
            binary_name = values["binary_name"]
            print("==================================================================")
            print("Passed build values are")
            print("plugin_name: "+i["name"]+"\n")
            print("version: "+str(version)+"\n")
            print("binary_name: "+binary_name)
            print("==================================================================")
        except TypeError:
            version = "NA"
            binary_name = "NA"
            #print("repo_name="+i["repo_name"]+" version="+version)
        if version != "NA":
            global_manifest['packages'].append({ "name": "{}".format(i["repo_name"]), "type": "{}".format(i["type"]), "version": "{}".format(version), "sourceURL": "{{ downloadurl }}/Windows/{}/{}/{}".format(i["repo_name"], version,binary_name)})
    except KeyError:
        repo_name = i["repo_name"]
        ## get request to artifactory to get the version
        artifact_call = latest_build(repo_name)
        max_build_no = artifact_call.artifactory_call()
        version_call = windows_binary_version(repo_name,max_build_no)
        values = version_call.windows_binary_version_artifactory_call()
        version = values["version_value"]
        binary_name = values["binary_name"]
        print("==================================================================")
        print("The build is not passed..getting latest Released Build No.\n")
        print("plugin_name: "+i["name"]+"\n")
        print("version: "+str(version)+"\n")
        print("binary_name: "+binary_name)
        print("==================================================================")
        if version != "NA":
            global_manifest['packages'].append({ "name": "{}".format(repo_name), "type": "{}".format(i["type"]), "version": "{}".format(version), "sourceURL": "{{ downloadurl }}/Windows/{}/{}/{}".format(repo_name, version,binary_name)})

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
