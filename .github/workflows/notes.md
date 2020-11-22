
Would like to using github action:

1. On a change in master
2. reformat the changed files
3. Send changes to PVL

Limitation

1. Do not think that I figured out how to link to master on github actions. 
2. Can not commit files from master, as they 


# Current process

Occurs locally:
0. Removes everything in Database/Si. 
1. Merge master into github actions. All or Diff, doesn't matter. Currently doing all. 
2. Run script yaml2json.py:
	* it recognises the master files (from file path), and gets their info
	* It deletes the contence of the corresponding folder, corresponding to the masters file name
	* It does not check for linked names.
	* It remakes the contence of the folder, from the .srh files from the master. Here it uses linked names.
	* It removes the master files 
7. At this point we have everything in the correct format, so we can add everything and commit. 
2. We push online, and changes are sent to PVL. This compares the commit to the last, and pushes it. In this way its important that each and every commit is pushed. 

Checked:

1. Additions
2. Modification
3. Deletions

limitations:
	currently can not detele if an entire file has been deleted. This can be added by adding an empty file with the folder name. Need to have a script that detects these from the main. the other suggestion is to just remove everything and rebuild it all. 
	Need to update field names, so the render correctly on the website
	
 
