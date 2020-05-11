
import yaml
import json
import os
import glob

def yamlFile2Jsons(fname):
    '''
    Given a file name returns a list of authors and JSON dics.
    This only returns the file name of the new file, not the folder location
    '''
    lst = []
    if '.srh' in fname:
        with open(fname, 'r') as f:
            a = yaml.load(f, Loader=yaml.FullLoader)

        for k,v in a.items():
            lst.append((k+'.srh', json.dumps(v, indent=4)))

    return lst

def createNewFiles(folder, fnames):
    '''
    takes a list of touples. 
    file names and creates them

    inputs:
    ------
    folder: (str)
        The folder path to be saved at
    fname: (list of touples)
        This is a list of touples. The first is the file name the second is the contence.
    '''
    # makes the folder if
    if not os.path.exists(folder):
        os.mkdir(folder)
    # makes the files
    for fname in fnames:
       path = os.path.join(folder, fname[0])
       with open(path, 'w+') as f:
            f.write(fname[1])

def yaml2json():
    
    for fname in glob.glob('./database/*/*/*.srh'):
        folder = fname.replace('.srh', '') 
        fnames = yamlFile2Jsons(fname)
        createNewFiles(folder, fnames)
        os.remove(fname)
        

    for fname in glob.glob('./database/*/*/*.opt'):
        os.remove(fname)

    for fname in glob.glob('./database/*/*/*.pl'):
        os.remove(fname)

if __name__ == '__main__':
#    fname = '/home/arch/Dropbox/CommonCode/semiconductorDefects/database/Si/Fe/Fe_i_d.srh'
#    folder = fname.replace('.srh', '') 
#    fnames = yamlFile2Jsons(fname)
#    createNewFiles(folder, fnames)
    yaml2json()
