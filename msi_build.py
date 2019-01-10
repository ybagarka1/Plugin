#!/cygdrive/c/Users/yash.bagarka/AppData/Local/Programs/Python/Python36/python
import json
import requests, zipfile, io 
from jinja2 import Template
import os
from artifactory import ArtifactoryPath
from requests.auth import HTTPBasicAuth
import sys
from flask import Flask, render_template

downloadurl = 'http://update.dtitsupport247.net/InstallJunoAgent/Plugin'
artifactory_url = 'http://artifact.corp.continuum.net:8081'
artifactory_password = 'AP49A5SMDpZuQb7e9g7Tn5c45fbUfJkZMzmUSM' 

#artifactory_url = 'http://artifact.corp.continuum.net:8081'
artifactory_url = os.environ['artifactory_url']
# artifactory user name
artifactory_username = 'repluser'
# artifactoy password
artifactory_password = os.environ['artifactory_password']
# repo name for downlaoding
repo_name = 'int-dev_platform-agent-package'

#run time parameter from jenkins
build_no = 94

#downloading manifest json template from aritfactory

manifest_json = requests.get("{}/artifactory/{}/{}/globalmanifest.json.template".format(artifactory_url,repo_name,build_no), auth=HTTPBasicAuth(artifactory_username,artifactory_password))
global_manifest_template = json.loads(manifest_json.content)
print(global_manifest_template)
print("sourcing global manifest json file")
global_manifest_template = Template("{}".format(global_manifest_template))
global_manifest_int = global_manifest_template.render(downloadurl = downloadurl)
for i in global_manifest_int['packages']:
    print(i['packages'])
#    plugin_req = requests.get(key['sourceURL'])
#    z = plugin_req.content

