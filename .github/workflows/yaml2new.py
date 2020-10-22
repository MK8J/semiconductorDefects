
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
    This returns the file name of the new file, not the folder location

    Parameters
    ----------
        a file name of a srh file.


    Returns
    -------
        A list of touples. The first item is the file name, the second is a dictionary containing the data.
    '''
    lst = []
    if '.srh' in fname:
        with open(fname, 'r') as f:
            a = yaml.load(f, Loader=yaml.FullLoader)

       
        if a is not None:
            for k, v in a.items():
                lst.append((k + '.srh', v))

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
        The folder path for the new data to be saved
    fname: (list of touples)
        This is a list of touples. The first is the file name the second is the contence.
        If an empty list is passed, the above folder is cleared
    '''
    # first thing to do is remove the folder if it exist
    # we are about to repopulate it with everything in the current file

    if os.path.exists(folder):
        print('folder being removed {}'.format(os.path.join(folder, '*')))

        os.system('rm {}'.format(os.path.join(folder, '*')))

    # makes the files
    for fname in fnames:
        # get right folder
        _folder = folder.split(os.sep)
        #print(_folder)
        


        if "linked" in fname[1].keys():
            dft = fname[1]['linked'].replace('.srh', '')
        else:
            dft = _folder[-1]

        # now we enforce unique defect names. Alphabetical, and metals first.
        elms = re.findall('[A-Z][^A-Z_]*', dft)
        sindex = sorted(range(len(elms)), key=lambda k: elms[k])

        #print(sindex, 'sindex', elms)
        # find elemnts that are non-metals
        # as these names go at the end
        Nonmetals = []
        Metals = []
        for num in sindex:
            if elms[num].strip('x') in nonmetals:
                Nonmetals.append(num)
            else:
                Metals.append(num)

        # get the states and change states
        states = dft.split('_')[1].split('-')

        final = dft.split('_')[2]
        # print(elms, sindex, Metals, Nonmetals, len(states), states, dft)
        # now build the last folder name
        _f = ''
        first = None
        for j in Metals:
            _f += elms[j]
            if first is None:
                first = elms[j].strip('x')


        for j in Nonmetals:
            _f += elms[j]
            if first is None:
                first = elms[j].strip('x')


        _f += '_'

        for j in Metals:
                _f += states[j]

        for j in Nonmetals:
                _f += states[j]

        _f = _f + '_' + final
        _folder[-1] = _f

        # the defect goes under first sorted alphbeticall metal then nonmetal
        elms = re.findall('[A-Z][^A-Z_]*', dft)
        _folder[-2] = re.sub('[0-9]', '', first)

        # finially makes
        #print('folder recreated', _folder)
        _folder = os.sep.join(_folder)
        # print(folder, _folder)

        # makes the folder if
        f = _folder
        if not os.path.exists(_folder):

            names = _folder.split(os.sep)

            for i in range(1, len(names)):
                #print(os.sep, names, names[:-i])
                f = '{}'.format(os.sep).join(names[:-i])
                #print(f, type(f))
                if os.path.exists(f):
                    break

            for j in range(1,i)[::-1]:
                f = '{}'.format(os.sep).join(names[:-j])
                #print('\n\tcreating', f, _folder)
                if not os.path.exists(f):
                        os.mkdir(f)

            os.mkdir(_folder)

        path = os.path.join(_folder, fname[0])
        with open(path, 'w+') as f:
            f.write(json.dumps(fname[1], indent=4))


def yaml2json(commit=True):
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
    #print('converting files')
    for fname in glob.glob('./database/*/*/*.srh'):
        print(fname, 'fname')
        folder = fname.replace('.srh', '')
        fnames = add_DLTS_params(yamlFile2Jsons(fname))

        print('recied fnames', fnames)
        createNewFiles(folder, fnames)

        # remove the files from master
        os.remove(fname)
        # prune them from git tracking
        os.system('git rm {}'.format(fname))

    #if commit:
    #    os.system('git add -A')
    #    os.system('git commit -m "auto commit - added new files"')
    #    os.system('git push origin')

    print('pruning other files')
    # removes optical file contences, as this is not used
    for fname in glob.glob('./database/*/*/*.opt'):
        os.remove(fname)
        os.system('git rm {}'.format(fname))

    # removes pl data as this is not used
    for fname in glob.glob('./database/*/*/*.pl'):
        os.remove(fname)
        os.system('git rm {}'.format(fname))

    # commits the remove items that should not be on this branch.
    # that means, from here on a diff works to compare files that
    # have changes on this branch 
    
    if commit:
        os.system('git commit -m "auto commit: removed master branch files"')
        os.system('git push origin')
    

def check_temps():

    for fname in glob.glob('./database/*/*/*/*.srh'):
        #print(fname, end=(','))
        with open(fname, 'r') as f:
            cont = f.read()
        addTemps(json.loads(cont))
        #print('', end=('\r'))


def get_DLTS_params(temp, e_r):
    '''
    Determines the energy level and arhenious y-int from
    emission rate data by performing a linear fit to
    the log of the emission rate divided by the temperature squared
    versus inverse temprature:

        $ ln(e/T^2) = ln(int) + q/kT -Ed $
    Where int and Ed are found.


    Parameters
    ----------

    temp: (array like)
         A list of temperatures in Kelvin
    e_r: (array like)
         A list of emission rates in 1/s

    Returns
    -------
    inter:
         the y-intercept of the arhenious plot, with units /sK^2
    Activation energy:
         The activation energy of the defect
    '''

    temp = np.array(temp)
    e_r = np.array(e_r)

    A = C.e / C.k

    Ed, inter = np.polyfit(A / temp, np.log(e_r / temp**2), 1)
    Ed *= -1


    # limits the y-intercept to three sig fig
    sigfig = 3
    inter = np.exp(inter)
    inter = round(inter, -1 * int(np.log10(inter) // 1 - sigfig + 1))

    # these should be positive floats
    assert inter>0, 'inter below 0'
    assert Ed>0, 'Ed below 0'

    return inter, round(Ed, 3)

def add_DLTS_params(data_touple):
    '''
    given something

    adds:
        * temperature for specified emission rates
        * Acitivation energy and arhenious intercept calculated from the above


    Parameters
    ----------
        the output from yamlFile2Jsons. A list of touples. The first item is the file name, the second is a dictionary containing the data.

    Returns
    -------
        same as input, but the extra data
    '''

    e_r = np.array([1,10,100,1000])
    new_list = []

    for fname, data_dic in data_touple:
        DLTS_params = {}
        #print('\t\t',fname, end=('\t'))
        temps = getTemps(data_dic)

        # if we can cal temps
        if temps is not None:
            emn_temps = {'t{0}'.format(i+1):'{0:.1f}'.format(t) for i,t in enumerate(temps)}

            DLTS_params.update(emn_temps)

            # from this data, calculate the activation energy
            # and the y intercept
            #print('checking DLTS_params', type(temps), temps)
            #print(temps, e_r)
            inter, Ed = get_DLTS_params(temps, e_r)

            DLTS_params['inter'] = str(inter)
            DLTS_params['Ed_a'] = str(Ed)


                # append them to the dictionary Tags
            data_dic['DLTS_params'] = DLTS_params


        new_list.append((fname, data_dic))

    return new_list




def getTemps(JSONdata):
    '''
    Given the json content, determine the temperatures
    for the emission rates of 1,10,100,1000 1/s.

    The prefered way of calculations is:
    1. If measured emission data is provide use that
    2. Calculate it from the acitvation energy and apparent capture cross section.
        For this calculation we assume a T^2 dependence for material constants

    If the emission rate is above 500 K, the calculation may not find it.

    inputs
    -------
    JSONdata:
        the JSON data that is send to PVL. This is actually a dictionary.
        Confusion name I should change this.

    returns
    -------
    temps:
        An array of temperatures for the emission rates 1,10,100,1000.
        None is returned if they could not be calculated.
    '''

    er = np.array([1, 10, 100, 1000])
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
        #print('doing rates', end=('\t'))
        if 'e_e' in JSONdata['rates'].keys():
            e = JSONdata['rates']['e_e']
        elif 'e_h' in JSONdata['rates'].keys():
            e = JSONdata['rates']['e_h']

        #print(e, end=('\t'))
        #print(e)


        if type(e) == str:
            e = e.replace('^', "**")

            def fun(T, e_guess):

                k = C.k / C.e  # name important for eval function.
                kT = C.k / C.e * T  # name important for eval function.
                exp = np.exp
                # print(T, abs(eval(e) - e_guess), end=(',  '))
                return abs((eval(e) - e_guess)/e_guess)

            for _e in er:
                temps.append(minimize(fun, 500, args=(_e))['x'][0])


            assert all([temps[i]<temps[i+1] for i in range(len(temps)-1)]), 'error with temp cals :' + str(temps) +' ' + str(e)
    # if the activation energy level and capture cross sections are provided
    if 'params' in JSONdata.keys() and temps == []:
        eda = None
        sigma = None
        #print('doing params')
        if 'Ed_a' in JSONdata['params'].keys():

            if 'Ec' in JSONdata['params']['Ed_a'] and 'sigma_ea' in JSONdata['params'].keys():
                eda = abs(float(JSONdata['params']['Ed_a'].replace('Ec', '')))
                sigma = JSONdata['params']['sigma_ea']

                a = Nc * vthe / 300**2

            elif 'Ev' in JSONdata['params']['Ed_a'] and 'sigma_ha' in JSONdata['params'].keys():
                eda = abs(float(JSONdata['params']['Ed_a'].replace('Ev', '')))
                sigma = JSONdata['params']['sigma_ha']

                a = Nv * vthh / 300**2

            if type(sigma) == str:

                k = C.k / C.e  # name important for eval function.
                kT = C.k / C.e  # name important for eval function.
                exp = np.exp

                #print(type(sigma), sigma)
                try:
                    sigma = float(eval(sigma.replace('>', '')))

                except:
                    print(type(sigma), sigma)
                    sigma = None

            elif sigma is not None:
                sigma = float(sigma)

        if eda is not None and sigma is not None:
            b = eda / C.k * C.e
            a *= sigma / er

            #T = b/2/lambertw(b/2/np.sqrt(a))
            temps = b / 2 / lambertw(-np.sqrt(a) * b / 2).real

    if temps == []:
        temps = None
    else:
        temps = np.array(temps)


    return temps

if __name__ == '__main__':
    #    fname = '/home/arch/Dropbox/CommonCode/semiconductorDefects/database/Si/Fe/Fe_i_d.srh'
    #    folder = fname.replace('.srh', '')
    #    fnames = yamlFile2Jsons(fname)
    #    createNewFiles(folder, fnames)
    #    this is the one to uncomment
    yaml2json()
