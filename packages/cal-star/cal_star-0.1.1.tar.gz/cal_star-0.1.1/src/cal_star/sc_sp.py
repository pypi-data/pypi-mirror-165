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
        if starlist in ['Hamuy1992',
                        'oke1990',
                        'Massey1998',
                        'gemini',
                        'ctiocal',
                        'spec50cal']:            
            template_filename = os.path.join(refdata, '1d_sp', starlist, star+'.dat')
            cat = pd.read_csv(template_filename, sep='\s+')
            template_wave = cat.iloc[:,0].values      # unit should be in Angstrom
            template_flux = cat.iloc[:,1].values      # unit should be in erg/s/cm^2/A    
        else:
            raise ValueError("starlist or star name wrong. ")
        self.wave = template_wave
        self.flux = template_flux
        
#    def sp_plot(template_wave,template_flux):
#            template_wave = cat[0]      # unit should be in Angstrom
#            template_flux = cat[1]      # unit should be in erg/s/cm^2/A

    def get_wavestep(self):
        wave_start = self.wave
        wave_end = self.flux
        ws = template_wave.shape    # ws： wave step
        wr = wave_end - wave_start  # wr： wave range
        wave_delta = wr / ws
        return wave_delta

       
def default_sp(starlist,star):
    starlist = 'Hamuy1992'
    star = 'CD -34 241'   
    template_filename = os.path.join(refdata, '1d_sp', starlist,star + '.dat')
    cat = pd.read_csv(template_filename, sep='\s+')
    template_wave = cat.iloc[:,0].values      # unit should be in Angstrom
    template_flux = cat.iloc[:,1].values      # unit should be in erg/s/cm^2/A 
    listname = os.path.join(refdata, 'starlists', starlist,starlist + '.xlsx')
    df=pd.read_excel(listname)
    print(df)   
    return template_wave,template_flux

def star_sp(starlist,star):
    starlist = starlist
    star = star  
    template_filename = os.path.join(refdata, '1d_sp', starlist,star + '.dat')
    cat = pd.read_csv(template_filename, sep='\s+')
    template_wave = cat.iloc[:,0].values      # unit should be in Angstrom
    template_flux = cat.iloc[:,1].values      # unit should be in erg/s/cm^2/A 
    listname = os.path.join(refdata, 'starlists', starlist,starlist + '.xlsx')
    df=pd.read_excel(listname)
    print(df)   
    return template_wave,template_flux