
Would like to using github action:

1. On a change in master
2. reformat the changed files
3. Send changes to PVL

Limitation

1. Do not think that I figured out how to link to master on github actions. 
2. Can not commit files from master, as they 


# Current process

1. Merge master into github actions. All or Diff, doesn't matter. Currently doing all. 
2. Commit and push to online. 
3. From there a few things happens:
	* it recognises the master files (from file path)
	* It deletes the contence of folder that the file we be placed in
	* It remakes the contence of the folder. This is so deletes can be tracked
	* It removes the master files from the git tracking and commits and saves them. 
	* It then diffs. 
4. It then compares the diff to the upstream (the last commit). This will show any changes in the files are to be send to PVL. It then attempts to send them. 


Checked:

1. Additions
2. Modification
3. Deletions

 
