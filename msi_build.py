#!/cygdrive/c/Users/yash.bagarka/AppData/Local/Programs/Python/Python36/python
import json
import requests
from jinja2 import Template
downloadurl = "http://update.dtitsupport247.net/InstallJunoAgent/Plugin"
print("sourcing global manifest json file")
with open('globalmanifest.json.template', 'r') as f:
    global_manifest_template = json.load(f)
print(global_manifest_template)

for packages in global_manifest_template['packages']:
    print(packages['sourceURL'])
    download_plugin = requests.get("{}".format(packages['sourceURL']))
    print(download_plugin)
