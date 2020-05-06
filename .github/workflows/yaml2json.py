
import yaml
import json
import os


def yamlFile2Jsons(fname):
    '''
    Given a file name returns a list of authors and JSON dics.

    '''
    lst = []
    if '.srh' in fname:
        with open(fname, 'r') as f:
            a = yaml.load(f, Loader=yaml.FullLoader)

        for k,v in a.items():
            lst.append((fname.replace('.srh', os.sep+k+'.srh'), json.dumps(v)))

    return lst


if __name__ == '__main__':
    fname = '/home/arch/Dropbox/CommonCode/semiconductorDefects/database/Si/Fe/Fe_i_d.srh'

    print(yamlFile2Jsons(fname))
