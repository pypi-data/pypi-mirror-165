# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:13:49 2022

@author: Liang Yu

This code is used for showing the clusters.
by Yu Liang 
yuliang@shao.ac.cn
"""
import matplotlib.pyplot as plt
import os
import skimage.io as io 
from astropy.io import fits
import pandas as pd


path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
refdata = os.path.join(path, r'cal_star\refdata')
       
def default_cluster(cluster,filename,c1,l1,stp):
    cluster = 'NGC6397'
    filename = 'tif_infor' 
    strt  = os.path.join(refdata,'clusters',cluster, '*.tif')
    collt = io.ImageCollection(strt) 
    print('len of dir tiff files:',len(collt)) 
    strf  = os.path.join(refdata,'clusters',cluster, '*.fits')
    collf = io.ImageCollection(strf) 
    print('len of dir fits files:',len(collf)) 
    dirc  = os.path.join(refdata,'clusters',cluster)
    listc = os.listdir(dirc)
    print(listc)
    
    listname = os.path.join(refdata,'clusters',cluster, filename + '.xlsx')
    df=pd.read_excel(listname)
    print(df)   
    
    img = collt[0]
    print(img.shape)
    
    c1,l1 = 1272,2132
    stp = 240
    
    imgcut = img[l1:l1 + stp,c1:c1 + stp]
    plt.figure(num = 'IMGcut',figsize = [14,9]) 
    plt.subplot(121)
    plt.imshow(img,origin = 'lower')
    plt.title(cluster)
    plt.tight_layout()
    plt.xlabel('1.56 arcmin')
    plt.ylabel('2.11 arcmin')
    ax = plt.gca()
    ax.add_patch(plt.Rectangle((c1,l1),stp,stp, color="red", fill=False, linewidth=1.5))
    plt.subplot(122)
    plt.imshow(imgcut,origin = 'lower')
    plt.title(cluster)
    plt.tight_layout()
    plt.xlabel('6 arcsec')
    plt.ylabel('6 arcsec')
    return img,imgcut


def cluster_infor(cluster,filename):
    cluster = cluster
    filename = filename   
    strt  = os.path.join(refdata,'clusters',cluster, '*.tif')
    collt = io.ImageCollection(strt) 
    print('len of dir tiff files:',len(collt)) 
    strf  = os.path.join(refdata,'clusters',cluster, '*.fits')
    collf = io.ImageCollection(strf) 
    print('len of dir fits files:',len(collf)) 
    dirc  = os.path.join(refdata,'clusters',cluster)
    listc = os.listdir(dirc)
    print(listc)
    
    listname = os.path.join(refdata,'clusters',cluster, filename + '.xlsx')
    df=pd.read_excel(listname)
    print(df)   
    
    img = collt[0]
    print(img.shape)
    
    plt.figure(num = 'IMGshow',figsize = [14,9]) 
    plt.imshow(img,origin = 'lower')
    plt.title(cluster)
    plt.tight_layout()


def show_cluster(cluster,c1,l1,stp):
    print('c1,c2,stp, represent the star line, column, and step length in pixel respectively.')
    cluster = cluster  
    c1,l1 = c1,l1
    stp = stp
    strt  = os.path.join(refdata,'clusters',cluster, '*.tif')
    collt = io.ImageCollection(strt) 
    print('len of dir tiff files:',len(collt)) 
    strf  = os.path.join(refdata,'clusters',cluster, '*.fits')
    collf = io.ImageCollection(strf) 
    print('len of dir fits files:',len(collf)) 
    dirc  = os.path.join(refdata,'clusters',cluster)
    listc = os.listdir(dirc)
    print(listc)
    
    ltif = len(collt)
    if ltif == 0:
        hdu = fits.open(collf[0])
        img = hdu[1].data
        print(img.shape)
    else:
        img = collt[0]
        print(img.shape)

    imgcut = img[l1:l1 + stp,c1:c1 + stp]
    plt.figure(num = 'IMGcut',figsize = [14,9]) 
    plt.subplot(121)
    plt.imshow(img,origin = 'lower')
    plt.title(cluster)
    plt.tight_layout()
    plt.xlabel('1.56 arcmin')
    plt.ylabel('2.11 arcmin')
    ax = plt.gca()
    ax.add_patch(plt.Rectangle((c1,l1),stp,stp, color="red", fill=False, linewidth=1.5))
    plt.subplot(122)
    plt.imshow(imgcut,origin = 'lower')
    plt.title(cluster)
    plt.tight_layout()
    plt.xlabel('6 arcsec')
    plt.ylabel('6 arcsec')

    return img,imgcut