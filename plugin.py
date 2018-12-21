##!/bin/python2.7
from bs4 import BeautifulSoup
import requests
from array import *

		
header = { 'username': 'repluser', 'password': 'AP49A5SMDpZuQb7e9g7Tn5c45fbUfJkZMzmUSM', 'Content-Type' : 'application/json' }
response = requests.get('http://artifact.corp.continuum.net:8081/artifactory/dt-dev_platform-agent-core', data=header)
soup = BeautifulSoup(response.content, "html.parser")
b = soup.find_all("a")
data = []
builds = []
buildno = []
for tag in b:
	data=tag.attrs['href']
	builds = tag.attrs['href'].replace("/", "")
	buildno.append(int(builds))

latest_version = max(buildno)
print(latest_version)
