import img_scale
from numpy import *
import pylab
import scipy
import matplotlib.pyplot as plt
import scipy.ndimage as snd
from scipy.ndimage import interpolation
import calib4
from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import get_pkg_data_filename
import alignment5
import remove_deadhot

input1='n5719_b.lis'    #object with blue fliter list
input2='n5719_g.lis'    #object with green fliter list
input3='n5719_r.lis'    #object with red fliter list
input4='alldarkssmall.list' #dark list
input5='allbiassmall.list'  #bias list
input6='bflat.lis'  #blue flat field list
input7='gflat.lis'  #green flat field list
input8='rflat.lis'  #red flat field list


b, g, r=calib4.calibration(input1, input2, input3, input4, input5, input6, input7, input8)
hot_b,fixed_b = remove_deadhot.find_outlier_pixels(b/65536.0*255.0)
hot_g,fixed_g = remove_deadhot.find_outlier_pixels(g/65536.0*255.0)
hot_r,fixed_r = remove_deadhot.find_outlier_pixels(r/65536.0*255.0)


newb, newg, newr=alignment5.alignment(fixed_b,fixed_g,fixed_r)
biasfiles=[line.rstrip('\n') for line in open(input1)]

cat=get_pkg_data_filename(biasfiles[0])
hdu=fits.open(cat)[0]
wcs=WCS(hdu.header)
n1=int(hdu.header['NAXIS1'])
n2=int(hdu.header['NAXIS2'])
bmin,bmax=newb.mean()-2.0*newb.std(),newb.mean()+10*newb.std()
gmin,gmax=newg.mean()-2.0*newg.std(),newg.mean()+10*newg.std()
rmin,rmax=newr.mean()-2.0*newr.std(),newr.mean()+10*newr.std()
img=zeros((n1,n2,3))
img[:,:,2]=img_scale.linear(newb,scale_min=bmin,scale_max=bmax)
img[:,:,1]=img_scale.linear(0.9*newg,scale_min=gmin,scale_max=gmax)
img[:,:,0]=img_scale.linear(newr,scale_min=rmin,scale_max=rmax)

fig=pylab.figure()
pylab.clf()
fig.add_subplot(111,projection=wcs)
pylab.xlabel('RA')
pylab.ylabel('DEC')
pylab.imshow(img,cmap=plt.cm.viridis)
fig.set_size_inches(10, 10, forward=True)
pylab.savefig('final_img')
pylab.close()

