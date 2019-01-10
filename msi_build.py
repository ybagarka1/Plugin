#!/cygdrive/c/Users/yash.bagarka/AppData/Local/Programs/Python/Python36/python
import json
import requests, zipfile, io 
from jinja2 import Template
downloadurl = "http://update.dtitsupport247.net/InstallJunoAgent/Plugin"
print("sourcing global manifest json file")
filein = open('globalmanifest.json.template')
global_manifest_template = Template(filein.read())
global_manifest_int = json.loads(global_manifest_template.render(downloadurl = downloadurl ))

for key in global_manifest_int['packages']:
    print(key['sourceURL'])
    plugin_req = requests.get(key['sourceURL'])
    z = zipfile.ZipFile(io.BytesIO(plugin_req.content))
    z.extractall()
