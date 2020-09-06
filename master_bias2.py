from astropy.io import fits
import matplotlib
matplotlib.use("TkAgg")
from numpy import *
import pylab
import scipy
import matplotlib.pyplot as plt

def master_bias(input):
    biasfiles=[line.rstrip('\n') for line in open(input)]

    bias=[]
    for file in biasfiles:
        bias.append(fits.getdata('%s' % file))

    #print shape(bias)
    masterbias=median(bias,axis=0)
    #print shape(master_bias)

    header=fits.getheader(biasfiles[0])
    header['HISTORY']='Median combined'
    fits.writeto('bias.fits', masterbias, header, clobber=True)
    '''
    fig=pylab.figure()

    plt.imshow(master_bias,cmap='gray')
    pylab.title('Master Bias')
    pylab.savefig('master_bias')
    pylab.close()
    '''
    return (masterbias)
