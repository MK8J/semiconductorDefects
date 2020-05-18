#!/usr/bin/python

import argparse 
import json
import requests
import yaml2new as y2n # tempory

parser = argparse.ArgumentParser(description='Process repository changes')
parser.add_argument('-c', '--changes', required=True, help='a list of changes')
parser.add_argument('-u', '--username', required=True, help='username for login')
parser.add_argument('-p', '--password', required=True, help='password for login')


args = parser.parse_args()

class Tag:
    Key = ''
    Value = ''

class Defect:
    settingId = ''
    settingPath = ''
    Tags = [] # This is a list of tags
    JSONData = ''

changeslist = args.changes.splitlines()
# A: addition of a file

# C: copy of a file into a new one

# D: deletion of a file
# D     .github/workflows/testfile.txt

# M: modification of the contents or mode of a file

# R: renaming of a file
# R100  .github/workflows/testfile.txt  testfile.txt

# T: change in the type of the file

# U: file is unmerged (you must complete the merge before it can be committed)

# X: "unknown" change type (most probably a bug, please report it)


additions = [change.split() for change in changeslist if change.startswith("A")]

modifications = [change.split() for change in changeslist if change.startswith("M")]

deletions = [change.split() for change in changeslist if change.startswith("D")]

renames = [change.split() for change in changeslist if change.startswith("R")]



# get the authentication token
payload = {'grant_type':'password', 'username':args.username, 'password':args.password}
r = requests.post("https://www.pvlighthouse.com.au/Token", data=payload)

r.raise_for_status()

basePath = "https://k8s.pvlighthouse.com.au/svc/usersettings/defects"

accessToken = (r.json()['access_token'])

headers = headers = {"Authorization": "Bearer " + accessToken, 'Content-Type': 'application/json'} 

def handleHttpResponse(response, baseErrorMessage):
    print(response.status_code)
    if response.status_code == 200:
        return
    elif response.status_code == 404:
        print(baseErrorMessage + " setting not found")
        return
    elif response.status_code == 409:
        print(baseErrorMessage + " setting conflicts with existing setting")
        return
    elif response.status_code == 400:
        print(baseErrorMessage + " validation error")
        print(response.text)
        response.raise_for_status()
        return
    else:
        response.raise_for_status()

for deletion in deletions:
    print("deleting " + deletion[1])
    deleteRequest = requests.delete(basePath + "/" + deletion[1], headers=headers)
    handleHttpResponse(deleteRequest, "Could not delete " + deletion[1])


for rename in renames:
    print("renaming " + rename[1] + " to " + rename[2])
    # need to build the json here
    setting = Defect()
    setting.settingPath = rename[2]
    
    with open(rename[2], 'r') as f:
        JSONData = f.read()

    setting.JSONData = JSONData

    temps = y2n.getTemps(JSONData)
    if temps is not None:
        emn_temps = Tag()
        emn_temps.Key = "emn_temps"
        emn_temps.Value = Temps

    setting.Tags.append(emn_temps)
    renameRequest = requests.put(basePath + "/" + rename[1], data=json.dumps(setting.__dict__), headers=headers)
    handleHttpResponse(renameRequest, "Could not rename " + rename[1])

for modification in modifications:
    print("updating " + modification[1])
    # need to build the json here
    setting = Defect()
    setting.settingPath = modification[1]

    with open(modification[1], 'r') as f:
        JSONData = f.read()

    setting.JSONData = JSONData
    
    temps = y2n.getTemps(json.loads(JSONData))
    if temps is not None:
        emn_temps = Tag()
        emn_temps.Key = "emn_temps"
        emn_temps.Value = Temps

    setting.Tags.append(emn_temps)
    updateRequest = requests.put(basePath + "/" + modification[1], data=json.dumps(setting.__dict__), headers=headers)
    handleHttpResponse(updateRequest, "Could not update " + modification[1])

_sp = None 

for addition in additions:
    #print(addition)
    #print("adding " + addition[1])
    # need to build the json here
    setting = Defect()
    setting.settingPath = addition[1]

    #print(addition[1])
    with open(addition[1], 'r') as f:
        JSONData = f.read()

    setting.JSONData = JSONData

    sp = '/'.join(addition[1].split('/')[:-1])
    if sp != _sp:
        _sp = sp
        print( sp)
    
    temps = y2n.getTemps(json.loads(JSONData))
    if temps is not None:
        emn_temps = Tag()
        emn_temps.Key = "emn_temps"
        emn_temps.Value = temps

    print(json.dumps(setting.__dict__))
    #print('\t', addition[1].split('/')[-1],temps)
    additionRequest = requests.post(basePath, data=json.dumps(setting.__dict__), headers=headers)
    handleHttpResponse(additionRequest, "Could not create " + addition[1] )

