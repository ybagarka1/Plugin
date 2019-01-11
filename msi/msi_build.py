#!/cygdrive/c/Users/yash.bagarka/AppData/Local/Programs/Python/Python36/python
import json
import requests, zipfile, io 
from jinja2 import Template
import os
from artifactory import ArtifactoryPath
from requests.auth import HTTPBasicAuth
import sys
from flask import Flask, render_template

downloadurl = 'http://update.qaitsupport247.local/InstallJunoAgent/Plugin'

#artifactory_url = 'http://artifact.corp.continuum.net:8081'
artifactory_url = os.environ['artifactory_url']
# artifactory user name
artifactory_username = 'repluser'
# artifactoy password
artifactory_password = os.environ['artifactory_password']
# repo name for downlaoding
repo_name = 'int-dev_platform-agent-package'
# build no of the passed global manifest build
build_no = os.environ['GLOBAL_MANIFEST_BUILD_NUMBER']

#run time parameter from jenkins

#downloading manifest json template from aritfactory

manifest_json = requests.get("{}/artifactory/{}/{}/globalmanifest.json.template".format(artifactory_url,repo_name,build_no), auth=HTTPBasicAuth(artifactory_username,artifactory_password))
global_manifest_template = json.dumps(manifest_json.json())
print("sourcing global manifest json file")
global_manifest_template = Template("{}".format(global_manifest_template))
global_manifest_int = global_manifest_template.render(downloadurl = downloadurl)
global_manifest_int = json.loads(global_manifest_int)
for i in global_manifest_int['packages']:
    print(i['sourceURL'])
    plugin_req = requests.get(i['sourceURL'])
#    os.chdir('src/github.com/ContinuumLLC/platform-agent-core/package/wixmsifull/resource/')
    os.chdir("D:/Plugin/ITSPlatform")
    z = zipfile.ZipFile(io.BytesIO(plugin_req.content))
    plugin_req = requests.get(i['sourceURL'])
    z.extractall()

