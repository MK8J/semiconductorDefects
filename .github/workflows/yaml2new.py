
import yaml
import json
import os
import glob
import scipy.constants as C
from scipy.special import lambertw
from scipy.optimize import minimize
import numpy as np
import re

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
            lst.append((k+'.srh', ))

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

    # makes the files
    for fname in fnames:
       if "linked" in fname[1].keys():
           _folder = folder.split(os.sep)
           dft = fname[1]['linked'].replace('.srh','')
           elms = re.findall('[A-Z][^A-Z_]*')
           _folder[-2] = elms[1] 
           _folder[-1] = dft 
           print(folder, _folder, fname[1]['linked'])
    else:
        _folder = folder


    # makes the folder if
       if not os.path.exists(_folder):
            os.mkdir(_folder)
       path = os.path.join(folder, fname[0])
       with open(path, 'w+') as f:
            f.write(json.dumps(fname[1], indent=4))

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

def check_temps():
    
    for fname in glob.glob('./database/*/*/*/*.srh'):
        print(fname, end=(','))
        with open(fname, 'r') as f:
            cont = f.read()
        addTemps(json.loads(cont))
        print('', end=('\r'))


def addTemps(JSONdata):
    '''
    Given the json content, determine the temperatures 
    for the emission rates of 1,10,100,1000 1/s. 

    The prefered way of calculations is:
    1. If measured emission data is provide use that
    2. Calculate it from the acitvation energy and apparent capture cross section. 
        For this calculation we assume a T^2 dependence for material constants
    '''

    er = np.array([1,10,100,1000]) 
    temps = []
    # values at 300K.
    Nc = 2.89e19
    Nv = 3.14e19
    vthe = 2.046e7
    vthh = 1.688e7

    # if the rates are provided, use it.
    # these will have to be calculated
    if 'rates' in JSONdata.keys() and ('e_e' in JSONdata['rates'].keys() or 
            'e_h' in JSONdata['rates'].keys()):
       if 'e_e' in JSONdata['rates'].keys():
            e = JSONdata['rates']['e_e']
       elif 'e_h' in JSONdata['rates'].keys():
            e = JSONdata['rates']['e_h']

       if type(e)==str:
           e=e.replace('^', "**")

           def fun(T, e_guess):

               k = C.k/C.e # name important for eval function. 
               kT = C.k/C.e*T # name important for eval function. 
               exp = np.exp
               return abs(eval(e)-e_guess)

           for _e in er:
               temps.append(minimize(fun, 300, args=(_e))['x'][0])



    # if the activation energy level and capture cross sections are provided
    if 'params' in JSONdata.keys() and temps == []:
        eda = None
        sigma = None
        if 'Ed_a' in JSONdata['params'].keys():
            
            if 'Ec' in JSONdata['params']['Ed_a'] and 'sigma_ea' in JSONdata['params'].keys():
                eda = abs(float(JSONdata['params']['Ed_a'].replace('Ec', '')))
                sigma = JSONdata['params']['sigma_ea']



                a = Nc*vthe/300**2

            elif 'Ev' in JSONdata['params']['Ed_a'] and 'sigma_ha' in JSONdata['params'].keys():
                eda = abs(float(JSONdata['params']['Ed_a'].replace('Ev', '')))
                sigma = JSONdata['params']['sigma_ha']


                a = Nv*vthh/300**2

            if type(sigma) == str:

               k = C.k/C.e # name important for eval function. 
               kT = C.k/C.e # name important for eval function. 
               exp = np.exp

               #print(type(sigma), sigma)
               try:
                   sigma = float(eval(sigma.replace('>', '')))

               except:
                   print(type(sigma), sigma)
                   sigma=None

            elif sigma is not None:
                sigma = float(sigma)


        if eda is not None and sigma is not None:
            b = eda/C.k*C.e 
            a *= sigma/er

            #T = b/2/lambertw(b/2/np.sqrt(a))
            temps = b/2/lambertw(-np.sqrt(a)*b/2).real

    return temps



if __name__ == '__main__':
#    fname = '/home/arch/Dropbox/CommonCode/semiconductorDefects/database/Si/Fe/Fe_i_d.srh'
#    folder = fname.replace('.srh', '') 
#    fnames = yamlFile2Jsons(fname)
#    createNewFiles(folder, fnames)
# this is the one to uncomment
#    yaml2json()

    JSONdata1 ={
    "title": "A quenched-in defect in boron-doped silicon",
    "DOI": "10.1063/1.323505",
    "measurement_technique": "DLTS",
    "sample": {
        "growth": "FZ, CZ",
        "dopant": "boron",
        "resistivity": "1-100"
    },
    "params": {
        "Ed_a": "Ev+0.438",
        "sigma_ha": "2.269e-16"
    }
    }

    JSONdata2 ={
    "title": "Dotierungseigenschaften von Eisen in Silizium",
    "DOI": "10.1002/pssa.2210640123",
    "measurement_technique": "DLTS-CrMe, TS-C",
    "comments": "Capture cross sections manually extracted from figure, rates from digitisation of figure 10.",
    "rates": {
        "e_h": "2121999 * T^2 * exp(-0.435/kT)"
    },
    "params": {
        "Ed_a": "Ev+0.43",
        "Ed_h": "Ev+0.39",
        "sigma_e": "1.03e-10*T^(-1.506)",
        "sigma_h": "7.87e-20*exp(0.0221*T)+1.78e-17"
    }
    } 

    JSONdata3 = {
    "title": "Interstitial iron and iron-acceptor pairs in silicon",
    "DOI": "10.1007/BF00619081",
    "measurement_technique": "DLTS-Cr",
    "sample": {
        "growth": "FZ",
        "dopant": "aluminium, boron, gallium",
        "incorporation": "thermal",
        "resistivity": "0.3-100"
    },
    "rates": {
        "e_h": "1.603e6*T^2*exp(-0.43/kT)"
    },
    "params": {
        "Ed_h": "Ev+0.39",
        "dEd_h": 0.02,
        "sigma_h": "1.6e-16*exp(-0.043/k/T)"
    }
    }
#    print(addTemps(JSONdata1))
    
    check_temps()
#    print(addTemps(JSONdata2))

