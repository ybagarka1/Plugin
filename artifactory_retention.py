##!/usr/local/bin/python3.5
#### Author: Yash Bagarka ####
#### Purpose: Artifactory Retention Policy ####
import requests
import json
import sys
import os
from artifactory import ArtifactoryPath
from datetime import datetime, timedelta
artifactory_url = "http://artifact.corp.continuum.net:8081/artifactory"
## required variables
#artifactory_url = 'http://artifact.corp.continuum.net:8081'
artifactory_url = os.environ['artifactory_url']
#repo_name = ['dt-dev_its-portal-net','dt_dev_yash']
repo_name = os.environ['repo_name']
#retention_period = '8mo'
retention_period = os.environ['retention_period']

## to validate the retention period variable
if "mo" in retention_period or "w" in retention_period:
        print()
else:
        print("Exiting due to variable declaration issue")
        sys.exit()
repo_name = repo_name.split(',')
aql = ArtifactoryPath("{}/artifactory/".format(artifactory_url), auth=('repluser', 'AP49A5SMDpZuQb7e9g7Tn5c45fbUfJkZMzmUSM'))

# multiple repo list
for r in  repo_name:
    build_numbers = []
    artifacts = aql.aql("items.find", {"type":"folder","repo":"{}".format(r)})
    build_info = []
    for a in range(len(artifacts)):
        if (artifacts[a]["name"] != "."):
            build_info.append(int(artifacts[a]["name"]))
    build_max_no = max(build_info)
    for b in range(len(artifacts)):
        if (artifacts[b]["name"] != "." and build_max_no == int(artifacts[b]["name"])):
            created_date = artifacts[b]["created"]
            zulu_time,string,seconds = created_date.rpartition('-')
            zulu_time = zulu_time+'Z'
            utc_dt = datetime.strptime(zulu_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            #last_build_epoch = (utc_dt - datetime(1970, 1, 1)).total_seconds()
            retention_time = utc_dt - timedelta(14)
            #retention_build_epoch =  (past_time - datetime(1970, 1, 1)).total_seconds()
            with open('{}.delete_info'.format(r), 'w') as outfile:
                outfile.write("latest_build_no={},retention_build_date={}".format(build_max_no, retention_time))

for z in repo_name:
    with open('{}.delete_info'.format(z), 'r') as file:
        ret_time = file.read()
        build_no, ret_time = ret_time.split(',')
        ret_time = ret_time.replace(' ','T')
        ret_time = ret_time.split('=', 1)[1]
        print("repo_name="+z)
    artifacts = aql.aql("items.find", {"type":"folder","repo":"{}".format(z),"created": { "$gt": "{}".format(ret_time)}})
    for list in range(len(artifacts)):
        if artifacts[list]["name"] != ".":
            print(artifacts[list]["name"])

sys.exit()
# logic to list all build numbers from the last created date
for c in repo_name:
    with open('{}.delete_info'.format(c), 'r') as readfile:
            max_build, long_epoch_created, long_epoch_retention = readfile.read().split(',')
            long_epoch_retention_mills, not_needed = long_epoch_retention.split('.')
            long_epoch_created_mills, not_needed = long_epoch_created.split('.')
            constant, append_created_info = (long_epoch_retention_mills + '000').split('=')
            constant, append_retention_info = (long_epoch_created_mills + '000').split('=')
            response = requests.get('{}/artifactory/api/search/creation?from={}&to={}&repos={}'.format(artifactory_url, append_created_info, append_retention_info, c),auth=('repluser', 'AP49A5SMDpZuQb7e9g7Tn5c45fbUfJkZMzmUSM'))
            for d in range(len(response.content)):
                print(response.content)

#for element in range(len(artifacts)):
#            if (artifacts[element]["type"] == "folder" and artifacts[element]["name"] != "."):
#                    build_numbers.append(int(artifacts[element]["name"]))
sys.exit()
build_numbers.sort(key=int)
print("List of builds that needs to be deleted post sorting")
for i in build_numbers:
        print(i)
#       response = requests.delete('{}/api/build/{}?buildNumbers={}&artifacts=1'.format(artifactory_url,repo_name,i),auth=('repluser', 'AP49A5SMDpZuQb7e9g7Tn5c45fbUfJkZMzmUSM'))

#       response = requests.delete('{}/artifactory/{}/{}'.format(artifactory_url,repo_name,i),auth=('repluser', 'AP49A5SMDpZuQb7e9g7Tn5c45fbUfJkZMzmUSM'))
