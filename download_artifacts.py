#!/cygdrive/c/Users/yash.bagarka/AppData/Local/Programs/Python/Python36/python
import requests
import json
import sys
import os
from artifactory import ArtifactoryPath
from datetime import datetime, timedelta

## required variables
#artifactory_url = 'http://artifact.corp.continuum.net:8081'
artifactory_url = os.environ['artifactory_url']
# artifactory user name
artifactory_username = 'repluser'
# artifactoy password
artifactory_password = os.environ['artifactory_password']
repo_name = "platform-version-plugin"
max_build_no = 54
#aql = ArtifactoryPath("{}/artifactory/api/archive/download/dt-dev_{}/{}".format(artifactory_url, repo_name, max_build_no),auth=('{}'.format(artifactory_username),'{}'.format(artifactory_password)))
#aql = ArtifactoryPath("{}/artifactory/".format(artifactory_url),auth=('{}'.format(artifactory_username),'{}'.format(artifactory_password)))
#artifacts = aql.aql("archive.entries.find", {"archive.item.repo":"dt-dev_{}".format(repo_name)})
header = { 'username': 'repluser', 'password': 'AP49A5SMDpZuQb7e9g7Tn5c45fbUfJkZMzmUSM', 'Content-Type' : 'application/json' }
url = "http://artifact.corp.continuum.net:8081/artifactory/api/build/dev_{}/{}".format(repo_name,max_build_no)
print(url)
build_info_json = requests.get("http://artifact.corp.continuum.net:8081/artifactory/api/build/dev_{}/{}".format(repo_name,max_build_no), data=header)
print(build_info_json.content)
