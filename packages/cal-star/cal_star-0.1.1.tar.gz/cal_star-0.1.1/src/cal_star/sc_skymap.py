# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 10:33:40 2022

@author: Liang Yu

This code is used for setting the spce_cal parameters.
by Yu Liang 
yuliang@shao.ac.cn
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import astropy.io.fits as fits
from scipy.integrate import simps
import extinction
import pdb
import functools

path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
refdata = os.path.join(path, r'cal_star\refdata')

class spec_map(object):

    r"""
    get spectrum template using the input parameters

    .. todo::
        enable to add emission lines


    Args:
        isource (dict, including 3 keys):
            name:
                the spectrum filename
            redshift:
                the redshift applied to the template
            ebv:
                the extinction applied to the template

    Attributes:

        wave (`numpy.ndarray`, unit in Angstrom):
            the wavelength of the spectrum, redshift applied.
        flux (`numpy.ndarray`, unit in erg/s/cm^2/A)
            the flux of the spectrum, redshift and extinction considered.

    """

    def __init__(self, starlist, star):

        starlist = starlist
        star = star   
        if starlist in ['Hamuy1992',
                        'oke1990',
                        'Massey1998',
                        'gemini',
                        'ctiocal',
                        'spec50cal']:            
            os.path.join(refdata,'starlists',starlist, starlist + '.xlsx')
            
            cat = pd.read_excel(template_filename)
            print(cat)
            
            ra = cat.iat[i,1]
            dec = cat.iat[i,2]   
        else:
            raise ValueError("starlist or star name wrong. ")
        self.ra = ra
        self.dec = dec
        self.cat = cat
        

def radec2plot(starlist, star):  # t2d: time to display ra map
    starlist = starlist
    star = star
    template_filename = os.path.join(refdata,'starlists',starlist, starlist + '.xlsx')
    df = pd.read_excel(template_filename) 
    col_data0 = df.iloc[:,0].values
    col_data0 = col_data0.tolist()
    i = col_data0.index(star)
    ra = df.iat[i,1]
    dec = df.iat[i,2]
    #display(ra.hour,ra.minute,ra.second,ra.microsecond)
    ram =  ra.hour + ra.minute / 60 + ra.second/3600
    deg = int(dec[0:3])
    arcm = int(dec[4:6])
    arcs = int(dec[7:10])
    if deg > 0:
        decm =  deg + arcm / 60 + arcs/3600
    else: 
        decm =  deg - arcm / 60 - arcs/3600

    plt.plot(ram,decm,'r*')
    return df, ram, decm

def radec2show(ra,dec):
    ram =  ra.hour + ra.minute / 60 + ra.second/3600
    deg = float(dec[0:3])
    arcm = float(dec[4:6])
    arcs = float(dec[7:10])
    if deg > 0:
        decm =  deg + arcm / 60 + arcs/3600
    else: 
        decm =  deg - arcm / 60 - arcs/3600
    return ram, decm
    
def shown_listinfor(starlist, star):
    starlist = starlist
    star = star   
    if starlist in ['Hamuy1992',
                    'oke1990',
                    'Massey1998',
                    'gemini',
                    'ctiocal',
                    'spec50cal']:            
        template_filename = os.path.join(refdata, 'starlists',starlist, starlist + '.xlsx')
        df = pd.read_excel(template_filename)
        print(df)
        
        # spec_map.__init__(starlist, star)
        # ram,decm = spec_map.radec2plot(self,starlist, star)
        # plt.plot(ram,decm,'r*', )

        # show star list map
        col_data0 = df.iloc[:,0].values
        a = col_data0.shape
        a1 = functools.reduce(lambda sub, ele: sub * 10 + ele, a)
        col_data0 = df.iloc[:,0].values
        col_data0.shape
        spinf = np.zeros([a1,2]) # spinf star position information
        for i in range(a1):
            ra = df.iat[i,1]
            dec = df.iat[i,2]
            ram,decm = radec2show(ra,dec)
            spinf[i,:] = ram,decm
    else:
        raise ValueError("it is a wrong starlist name.")
    return df, spinf   #,ram,decm