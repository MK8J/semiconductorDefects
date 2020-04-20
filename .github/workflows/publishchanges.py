#!/usr/bin/python

import argparse, requests 

parser = argparse.ArgumentParser(description='Process repository changes')
parser.add_argument('-c', '--changes', required=True, help='a list of changes')
parser.add_argument('-u', '--username', required=True, help='username for login')
parser.add_argument('-p', '--password', required=True, help='password for login')


args = parser.parse_args()


changeslist = args.changes.splitlines()

# A: addition of a file

# C: copy of a file into a new one

# D: deletion of a file

# M: modification of the contents or mode of a file

# R: renaming of a file
# R100  .github/workflows/testfile.txt  testfile.txt

# T: change in the type of the file

# U: file is unmerged (you must complete the merge before it can be committed)

# X: "unknown" change type (most probably a bug, please report it)

additions = list(filter(lambda chg: chg.startswith("A"), changeslist))
additions = list(map(lambda chg: chg.split()[-1], additions))

modifications = list(filter(lambda chg: chg.startswith("M"), changeslist))
modifications = list(map(lambda chg: chg.split()[-1], additions))

#need to deal with deletions too

# get the authentication token
payload = {'grant_type':'password', 'username':args.username, 'password':args.password}
r = requests.post("https://www.pvlighthouse.com.au/Token", data=payload)

r.raise_for_status()

print(r.json()['access_token'])

for change in changeslist:
    print (change)