
import yaml
import json
import os
import glob
import scipy.constants as C
from scipy.special import lambertw
from scipy.optimize import minimize
import numpy as np
import re

nonmetals = [
        'H', 'He',
        'B', 'C', 'N', 'O', 'F', 'Ne',
        'Si', 'P', 'S', 'Cl', 'Ar', 
        'Ge', 'As', 'Se', 'Br', 'Kr',
        'Sb', 'Te', 'I', 'Xe',
        'Po', 'At', 'Rn',
        'Uss', 'Uuo'
        ]

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
            lst.append((k+'.srh', v ))

    return lst

def createNewFiles(folder, fnames):
    '''
    takes a list of touples. 
    file names and creates them
    It makes sure every file is only in one location. Unlike in the repository where 
    they are in every location. 

    inputs:
    ------
    folder: (str)
        The folder path to be saved at
    fname: (list of touples)
        This is a list of touples. The first is the file name the second is the contence.
    '''

    # makes the files
    for fname in fnames:
       # get right folder
       _folder = folder.split(os.sep)

       if "linked" in fname[1].keys():
           dft = fname[1]['linked'].replace('.srh','')
       else:
           dft = _folder[-1]

       # now we enforce unique defect names. Alphabetical, and metals first.
       elms = re.findall('[A-Z][^A-Z_]*', dft)
       sindex = sorted(range(len(elms)), key=lambda k: elms[k])

       # find elemnts that are non-metals
       # as these names go at the end
       Nonmetals = []
       Metals = []
       for num, e in enumerate(elms):
           if e.strip('x') in nonmetals:
                Nonmetals.append(num)
           else:
               Metals.append(num)

       # get the states and change states 
       states = dft.split('_')[1].split('-') 

       final = dft.split('_')[2]
       print(elms, sindex, Metals, Nonmetals, len(states), states, dft)
       # now build the last folder name
       _f = ''
       for j in sindex:
           if j in Metals:
              _f +=  elms[j]
       for j in sindex:
           if j in Nonmetals:
              _f +=  elms[j]

       _f+='_'

       for j in sindex:
           if j in Metals:
              _f +=  states[j]
       for j in sindex:
           if j in Nonmetals:
              _f += states[j]
        
       _f = _f + '_' + final
       _folder[-1] = _f 
    
       # the defect goes under the first element 
       elms = re.findall('[A-Z][^A-Z_]*', dft)
       _folder[-2] = re.sub('[0-9]', '',elms[0].strip('x'))

       # finially makes
       _folder = os.sep.join(_folder)
       print(folder, _folder)

        # makes the folder if
       if not os.path.exists(_folder):
            os.mkdir(_folder)

       path = os.path.join(_folder, fname[0])
       with open(path, 'w+') as f:
            f.write(json.dumps(fname[1], indent=4))

def yaml2json():
    '''
    Changes the format of that database from YAML to JSON
    to aid in getting data on PV lighthouse. 
    
    It goes through the database folder and;
        Removes any .opt and .pl file that was in master
        For the .srh files in master, it extracts all the 
        authors, creates sub folders and then puts saves the same
        content for that author in that file as JSON.
    '''
    
    # converts all the author data from bring in one file
    # to being in individual files
    for fname in glob.glob('./database/*/*/*.srh'):
        folder = fname.replace('.srh', '') 
        fnames = yamlFile2Jsons(fname)
        createNewFiles(folder, fnames)
        os.remove(fname)
        
    # removes optical file contences, as this is not used
    for fname in glob.glob('./database/*/*/*.opt'):
        os.remove(fname)

    # removes pl data as this is not used
    for fname in glob.glob('./database/*/*/*.pl'):
        os.remove(fname)

def check_temps():
    
    for fname in glob.glob('./database/*/*/*/*.srh'):
        print(fname, end=(','))
        with open(fname, 'r') as f:
            cont = f.read()
        addTemps(json.loads(cont))
        print('', end=('\r'))

def get_DLTS_params(temp, e_r):
   '''
   Determines the energy level and arhenious y-int from
   emission rate data by performing a linear fit to 
   the log of the emission rate divided by the temperature squared 
   versus inverse temprature:

       $ ln(e/T^2) = ln(int) + q/kT -Ed $
   Where int and Ed are found. 

   inputs
   -------
   temp: (array like)
        A list of temperatures in Kelvin
   e_r: (array like)
        A list of emission rates in 1/s

   returns
   -------
   inter:
        the y-intercept of the arhenious plot, with units /sK^2
   Activation energy:
        The activation energy of the defect
   '''
   A = C.e/C.k

   Ed, inter  = np.polyfit(A/temp, np.log(e_r/temp**2), 1)

   # limits the y-intercept to three sig fig
   sigfig=3
   inter = np.exp(inter)
   inter = round(inter, -1*int(np.log10(inter)//1-sigfig+1)) 

   return  inter, round(Ed,3)


def getTemps(JSONdata):
    '''
    Given the json content, determine the temperatures 
    for the emission rates of 1,10,100,1000 1/s. 

    The prefered way of calculations is:
    1. If measured emission data is provide use that
    2. Calculate it from the acitvation energy and apparent capture cross section. 
        For this calculation we assume a T^2 dependence for material constants

    inputs
    -------
    JSONdata: 
        the JSON data that is send to PVL

    returns
    -------
    temps:
        An array of temperatures for the emission rates 1,10,100,1000.
        None is returned if they could not be calculated.
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

    if temps == []:
        temps = None

    return temps



if __name__ == '__main__':
#    fname = '/home/arch/Dropbox/CommonCode/semiconductorDefects/database/Si/Fe/Fe_i_d.srh'
#    folder = fname.replace('.srh', '') 
#    fnames = yamlFile2Jsons(fname)
#    createNewFiles(folder, fnames)
#    this is the one to uncomment
    yaml2json()

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
    
    #check_temps()
#    print(addTemps(JSONdata2))

