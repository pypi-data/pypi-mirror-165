# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 10:33:40 2022

@author: Liang Yu

This code is used for setting the spce_cal parameters.
by Yu Liang 
yuliang@shao.ac.cn
"""

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

class read_template(object):

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
        if starlist in ['Landolt1992'
                        ]:            
            os.path.join(refdata,'Photometric',starlist, starlist + '.xlsx')
            cat = pd.read_excel(template_filename, sep='\s+')
            print(cat)
            # template_wave = cat.iloc[:,0].values      # unit should be in Angstrom
            # template_flux = cat.iloc[:,1].values      # unit should be in erg/s/cm^2/A    
        else:
            raise ValueError("starlist or star name wrong. ")
        # self.wave = template_wave
        # self.flux = template_flux
        
#    def sp_plot(template_wave,template_flux):
#            template_wave = cat[0]      # unit should be in Angstrom
#            template_flux = cat[1]      # unit should be in erg/s/cm^2/A

    # def get_wavestep(self):
        # wave_start = self.wave
        # wave_end = self.flux
        # ws = template_wave.shape    # ws： wave step
        # wr = wave_end - wave_start  # wr： wave range
        # wave_delta = wr / ws
        # return wave_delta
        
def radec2float(ra,dec):
    h = float(ra[0:2])
    m = float(ra[2:4])
    s = float(ra[4:6])
    ram =  h + m / 60 + s/3600
    deg = float(dec[0:3])
    arcm = float(dec[3:5])
    arcs = float(dec[5:7])
    if deg > 0:
        decm =  deg + arcm / 60 + arcs/3600
    else: 
        decm =  deg - arcm / 60 - arcs/3600
    return ram, decm
       
def default_photometry(starlist,star):
    starlist = 'Landolt1992'
    star = 'WOLF 629'   
    template_filename = os.path.join(refdata, 'Photometric', starlist, starlist + '.xlsx')
    df = pd.read_excel(template_filename)
    print(df)
    # show star list map
    col_data0 = df.iloc[:,0].values
    a = col_data0.shape
    a1 = functools.reduce(lambda sub, ele: sub * 10 + ele, a)
    spinf = np.zeros([a1,2]) # spinf star position information

    for i in range(1,a1):
        rdinf = df.iat[i,1]
        ra = rdinf[0:8]
        dec = rdinf[8:18]
        #print(ra,dec)
        ra = ra.replace(" ", "")
        dec = dec.replace(" ", "")
        #print('new ra dec:',ra,dec)
        ram,decm = radec2float(ra,dec)
        spinf[i,:] = ram,decm
        print('star',i,'radec to float over!')
    # template_wave = cat.iloc[:,0].values      # unit should be in Angstrom
    # template_flux = cat.iloc[:,1].values      # unit should be in erg/s/cm^2/A 
    # listname = os.path.join(refdata, 'starlists', starlist,starlist + '.xlsx')
    # df=pd.read_excel(listname)
    # print(df)   
    return df, spinf   #,ram,decm