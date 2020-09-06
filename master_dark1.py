from astropy.io import fits
import matplotlib
matplotlib.use("TkAgg")
from numpy import *
import pylab
import scipy
import matplotlib.pyplot as plt
import math


def master_dark(input):
    darkfiles=[line.rstrip('\n') for line in open(input)]
    
    darks=[]
    for file in darkfiles:
        darks.append(fits.getdata('%s' % file))

    #print shape(darks)
    dark=median(darks,axis=0)
    #print shape(dark)

    header=fits.getheader(darkfiles[0])
    exptime=header['EXPTIME']
    header['HISTORY']='Median combined'
    fits.writeto('dark.fits', dark, header, clobber=True)
    '''
    fig=pylab.figure()

    plt.imshow(dark,cmap='gray')
    pylab.title('Master Dark')
    pylab.savefig('master_dark')
    pylab.close()
    '''
    return (dark, exptime)
