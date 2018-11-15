from astropy.io import fits
import numpy as np
import os
import pdb


def get_pixs_in_circ_aper(center_x,center_y,dim1,dim2,radius):
    if radius > 0:
        x0 = np.round(center_x-radius).astype(int)
        x1 = np.round(center_x+radius).astype(int)
        y0 = np.round(center_y-radius).astype(int)
        y1 = np.round(center_y+radius).astype(int)
    
    pixs_x = np.array([],dtype=int)
    pixs_y = np.array([],dtype=int)
    for ii in range(x0,x1):
        for jj in range(y0,y1):
            if np.sqrt( ((ii-center_x)**2.)+((jj-center_y)**2.) )<radius and ii > 0 and ii < dim1 and jj > 0 and jj < dim2:
                pixs_x = np.append(pixs_x,ii)
                pixs_y = np.append(pixs_y,jj)
                
    return((pixs_x,pixs_y))

def masking_regions(img,file_with_regions):
    if os.path.isfile(file_with_regions) == True:
        with open(file_with_regions,"r") as ff:
            for line in ff:
                if line.find("box") != -1:
                    params = line.split(",")
                    xc     = float(params[0][4:])
                    yc     = float(params[1])
                    lenght = float(params[2])
                    height = float(params[3])
                    x0 = np.round(xc-lenght/2).astype(int)
                    x1 = np.round(xc+lenght/2).astype(int)
                    y0 = np.round(yc-height/2).astype(int)
                    y1 = np.round(yc+height/2).astype(int)
                    img[y0:y1,x0:x1] = 0
                if line.find("circle") != -1:
                    params = line.split(",")
                    xc     = float(params[0][7:])
                    yc     = float(params[1])
                    radius = float(params[2][:-2])
                    pixels_x,pixels_y = get_pixs_in_circ_aper(xc,yc,img.shape[0],img.shape[1],radius)
                    for ii in range(len(pixels_x)):
                        img[pixels_y[ii],pixels_x[ii]] = 0

    return(img)
                
def unmasking_regions(img,file_with_regions):
    if os.path.isfile(file_with_regions) == True:
        with open(file_with_regions,"r") as ff:
            for line in ff:
                if line.find("box") != -1:
                    params = line.split(",")
                    xc     = float(params[0][4:])
                    yc     = float(params[1])
                    lenght = float(params[2])
                    height = float(params[3])
                    x0 = np.round(xc-lenght/2).astype(int)
                    x1 = np.round(xc+lenght/2).astype(int)
                    y0 = np.round(yc-height/2).astype(int)
                    y1 = np.round(yc+height/2).astype(int)
                    img[y0:y1,x0:x1] = 1
                if line.find("circle") != -1:
                    params = line.split(",")
                    xc     = float(params[0][7:])
                    yc     = float(params[1])
                    radius = float(params[2][:-2])
                    pixels_x,pixels_y = get_pixs_in_circ_aper(xc,yc,img.shape[0],img.shape[1],radius)
                    for ii in range(len(pixels_x)):
                        img[pixels_y[ii],pixels_x[ii]] = 1
    return(img)


file_regions_to_mask = "/media/fbuitrago/SAMSUNG/munich/running_mgefit/ds9_regions_to_mask_hst_image.reg"
file_regions_to_unmask = "/media/fbuitrago/SAMSUNG/munich/running_mgefit/ds9_regions_to_unmask_hst_image.reg"
old_mask = "/media/fbuitrago/SAMSUNG/munich/running_mgefit/running_sextractor_for_hst_image_my_mask/IC1101_hst_mask.fits"


hdu = fits.open(old_mask)
img = hdu[0].data
hdr = hdu[0].header

new_mask = masking_regions(img[:],file_regions_to_mask)

new_mask = unmasking_regions(new_mask[:],file_regions_to_unmask)

fits.writeto("./running_sextractor_for_hst_image_my_mask/new_mask_IC1101_hst.fits",new_mask,hdr,overwrite=True)

