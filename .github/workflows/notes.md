
Would like to using github action:

1. On a change in master
2. reformat the changed files
3. Send changes to PVL

Limitation

1. Do not think that I figured out how to link to master on github actions. 
2. Can not commit files from master, as they 


# Current process

1. Merge master into github actions. All or Diff, doesn't matter. Currently doing all. 
3. From there a few things happens. Run yaml2json.py:
	* it recognises the master files (from file path)
	* It deletes the contence of folder that the file we be placed in
	* It remakes the contence of the folder. This is so deletes can be tracked
	* It removes the master files 
7. At this point we have everything in the correct format, so we can add everything and commit. 
2. We push online, and changes are sent to PVL. Its important that each commit is sent. 

Checked:

1. Additions
2. Modification
3. Deletions

limitations:
	currently can not detele if an entire file has been deleted. This can be added by adding an empty file with the folder name. Need to have a scrit that detects these from the main 
	Need to update field names, so the render correctly on the website
 
