import numpy as np

def ids_as_str(ids):
    #it returns a numpy array of strings, when receiving the ids as float numbers
    ids = np.array(ids, dtype=np.str)
    ids[:] = [ele[:-2] for ele in ids]
    return ids

def finding_coo_max_pix(img):
	#it returns the x and y coordinates of the pixel with the maximum flux in a given image
    return np.unravel_index(np.nanargmax(img),img.shape)
    #np.nanargmax->gets the maximum element of the image without taking into account the NaN values
    #np.unravel_index->gets the two dimensional position from a coordinate in a flatten vector

#function that gets all the pixels within a given square aperture
#OUTPUT
#pixels_x and pixels_y: to get the all the pixels you need to do the permutations of these two variables
#flag_ok: tells you whether the squares were drawn within the limits of your image (0=no, 1=yes)
def get_pix_within_square_aper(center_x,center_y,dim1,dim2,aper_size_pix):
	#the aperture size must be divided to get the "radius", but remember it is a square
	offset = math.floor(aper_size_pix/2.)

	x0 = center_x - offset
	y0 = center_y - offset
	x1 = center_x + offset
	y1 = center_y + offset

	#I get the pixels
	pixels_x = np.arange(x0,x1)
	pixels_y = np.arange(y0,y1)

	#if the pixels do not clash with the image borders, flag_ok is equal to 1
	if np.all( [pixels_x >= 0,pixels_y >= 0,pixels_x < dim1,pixels_y < dim2] ):
		flag_ok = 1
	else:
		flag_ok = 0

	#as I will return pixels, it makes sense they are integer numbers
	pixels_x = pixels_x.astype(int)
	pixels_y = pixels_y.astype(int)

	return(flag_ok, pixels_x, pixels_y)

#resistant_mean function, a la IDL
#OUTPUT
#mean_objs_after_clipping: self-descriptive
#std_objs_after_clipping: self-descriptive
#scatter_objs_after_clipping: self-descriptive
def resistant_mean(vector,threshold):
	clipping_apers              = stt.sigmaclip(vector,low=threshold,high=threshold)
	objs_after_clipping         = clipping_apers[0] #objects after trimming
	mean_objs_after_clipping    = np.mean(objs_after_clipping)
	std_objs_after_clipping     = np.std(objs_after_clipping)
	scatter_objs_after_clipping = std_objs_after_clipping*np.sqrt(objs_after_clipping.size-1)

	return(mean_objs_after_clipping,std_objs_after_clipping,scatter_objs_after_clipping)
