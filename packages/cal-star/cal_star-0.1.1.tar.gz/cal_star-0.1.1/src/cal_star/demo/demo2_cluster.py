# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 09:34:34 2022

@author: DELL
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import cv2
import skimage.io as io 
from skimage import color
import math
from scipy import signal# misc
import imageio
# clusters shown

cluster = 'NGC6397'   # https://esahubble.org/images/heic0608b/
file = 'heic0608b'
path = os.path.abspath(os.path.join(os.getcwd(), ".."))
template_filename = os.path.join(path,'refdata\clusters',cluster, file + '.tiff')
strt  = os.path.join(path,'refdata\clusters',cluster, '*.tif')
collt = io.ImageCollection(strt) 
print('len of dir tiff files:',len(collt)) 
strf  = os.path.join(path,'refdata\clusters',cluster, '*.fits')
collf = io.ImageCollection(strf) 
print('len of dir fits files:',len(collf)) 
dirc  = os.path.join(path,'refdata\clusters',cluster)
listc = os.listdir(dirc)
print(listc)
print('##################### cluster information   ############################################')
print(' Position (RA):	17 40 58.39\n '' Position (Dec):	-53° 44 19.90 \n ' 'Field of view:	1.56 x 2.11 arcminutes\n Orientation:	North is 0.4° right of vertical' )

img = collt[0]
print(img.shape)

# =============================================================================
# plt.figure(num = 'IMG0_show',figsize = [10,8]) 
# plt.imshow(img,origin = 'lower')
# plt.title(cluster)
# #plt.axis('off')
# plt.tight_layout()
# plt.xlabel('1.56 arcmin')
# plt.ylabel('2.11 arcmin')
# 
# =============================================================================

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

c1,l1 = 2800,527
stp = 240
imgcut = img[l1:l1 + stp,c1:c1 + stp]
plt.figure(num = 'IMGcut2',figsize = [14,9]) 
plt.subplot(121)
plt.imshow(img,origin = 'lower')
plt.title(cluster)
plt.tight_layout()
plt.xlabel('1.56 arcmin')
plt.ylabel('2.11 arcmin')
ax = plt.gca()
ax.add_patch(plt.Rectangle((c1,l1),stp,stp, color="white", fill=False, linewidth=1.5))
plt.subplot(122)
plt.imshow(imgcut,origin = 'lower')
plt.title(cluster)
plt.tight_layout()
plt.xlabel('6 arcsec')
plt.ylabel('6 arcsec')



stop

# =============================================================================
# ####################################################################################
# # zoom test
# #######################################################################################
# from matplotlib.transforms import (
#     Bbox, TransformedBbox, blended_transform_factory)
# from mpl_toolkits.axes_grid1.inset_locator import (
#     BboxPatch, BboxConnector, BboxConnectorPatch)
# 
# 
# def connect_bbox(bbox1, bbox2,
#                  loc1a, loc2a, loc1b, loc2b,
#                  prop_lines, prop_patches=None):
#     if prop_patches is None:
#         prop_patches = {
#             **prop_lines,
#             "alpha": prop_lines.get("alpha", 1) * 0.2,
#             "clip_on": False,
#         }
# 
#     c1 = BboxConnector(
#         bbox1, bbox2, loc1=loc1a, loc2=loc2a, clip_on=False, **prop_lines)
#     c2 = BboxConnector(
#         bbox1, bbox2, loc1=loc1b, loc2=loc2b, clip_on=False, **prop_lines)
# 
#     bbox_patch1 = BboxPatch(bbox1, **prop_patches)
#     bbox_patch2 = BboxPatch(bbox2, **prop_patches)
# 
#     p = BboxConnectorPatch(bbox1, bbox2,
#                            # loc1a=3, loc2a=2, loc1b=4, loc2b=1,
#                            loc1a=loc1a, loc2a=loc2a, loc1b=loc1b, loc2b=loc2b,
#                            clip_on=False,
#                            **prop_patches)
# 
#     return c1, c2, bbox_patch1, bbox_patch2, p
# 
# 
# def zoom_effect01(ax1, ax2, xmin, xmax, **kwargs):
#     """
#     Connect *ax1* and *ax2*. The *xmin*-to-*xmax* range in both axes will
#     be marked.
# 
#     Parameters
#     ----------
#     ax1
#         The main axes.
#     ax2
#         The zoomed axes.
#     xmin, xmax
#         The limits of the colored area in both plot axes.
#     **kwargs
#         Arguments passed to the patch constructor.
#     """
# 
#     bbox = Bbox.from_extents(xmin, 0, xmax, 1)
# 
#     mybbox1 = TransformedBbox(bbox, ax1.get_xaxis_transform())
#     mybbox2 = TransformedBbox(bbox, ax2.get_xaxis_transform())
# 
#     prop_patches = {**kwargs, "ec": "none", "alpha": 0.2}
# 
#     c1, c2, bbox_patch1, bbox_patch2, p = connect_bbox(
#         mybbox1, mybbox2,
#         loc1a=3, loc2a=2, loc1b=4, loc2b=1,
#         prop_lines=kwargs, prop_patches=prop_patches)
# 
#     ax1.add_patch(bbox_patch1)
#     ax2.add_patch(bbox_patch2)
#     ax2.add_patch(c1)
#     ax2.add_patch(c2)
#     ax2.add_patch(p)
# 
#     return c1, c2, bbox_patch1, bbox_patch2, p
# 
# 
# def zoom_effect02(ax1, ax2, **kwargs):
#     """
#     ax1 : the main axes
#     ax1 : the zoomed axes
# 
#     Similar to zoom_effect01.  The xmin & xmax will be taken from the
#     ax1.viewLim.
#     """
# 
#     tt = ax1.transScale + (ax1.transLimits + ax2.transAxes)
#     trans = blended_transform_factory(ax2.transData, tt)
# 
#     mybbox1 = ax1.bbox
#     mybbox2 = TransformedBbox(ax1.viewLim, trans)
# 
#     prop_patches = {**kwargs, "ec": "none", "alpha": 0.2}
# 
#     c1, c2, bbox_patch1, bbox_patch2, p = connect_bbox(
#         mybbox1, mybbox2,
#         loc1a=3, loc2a=2, loc1b=4, loc2b=1,
#         prop_lines=kwargs, prop_patches=prop_patches)
# 
#     ax1.add_patch(bbox_patch1)
#     ax2.add_patch(bbox_patch2)
#     ax2.add_patch(c1)
#     ax2.add_patch(c2)
#     ax2.add_patch(p)
# 
#     return c1, c2, bbox_patch1, bbox_patch2, p
# 
# 
# axs = plt.figure().subplot_mosaic([
#     ["zoom1", "zoom2"],
#     ["main", "main"],
# ])
# 
# axs["main"].set(xlim=(0, 5))
# zoom_effect01(axs["zoom1"], axs["main"], 0.2, 0.8)
# axs["zoom2"].set(xlim=(2, 3))
# zoom_effect02(axs["zoom2"], axs["main"])
# 
# plt.show()
# 
# ####################################################################################
# # zoom test
# #######################################################################################
# =============================================================================
