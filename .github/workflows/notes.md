
Would like to using github action:

1. On a change in master
2. reformat the changed files
3. Send changes to PVL

Limitation

1. Do not think that I figured out how to link to master on github actions. 
2. Can not commit files from master, as they 


# Current process

1. Merge master into github actions. All or Diff, doesn't matter. Current;y doing all. 
2. commit and push to online. 
3. From there it recognises the master files (from file path), reads them, converts them, removes the master files from the git tracking and commits and saves them. 
4. It then compares the diff to the upstream (the last commit). This will show any changes in the files are to be send to PVL. It then attempts to send them. 


limitations:

1. It can't monitor deletes this way. It can it I delete a folder! 
 
