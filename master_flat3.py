from astropy.io import fits
import matplotlib
matplotlib.use("TkAgg")
from numpy import *
import pylab
import scipy
import matplotlib.pyplot as plt


def master_flat(inputb, inputg, inputr):
    bflatfiles=[line.rstrip('\n') for line in open(inputb)]
    gflatfiles=[line.rstrip('\n') for line in open(inputg)]
    rflatfiles=[line.rstrip('\n') for line in open(inputr)]


    bflats=[]
    gflats=[]
    rflats=[]

    for file in bflatfiles:
        bflats.append(fits.getdata('%s' % file))
    for file in gflatfiles:
        gflats.append(fits.getdata('%s' % file))
    for file in rflatfiles:
        rflats.append(fits.getdata('%s' % file))

#print shape(rflats)
    master_bflat=median(bflats,axis=0)
    master_gflat=median(gflats,axis=0)
    master_rflat=median(rflats,axis=0)
#print shape(master_bflat)

    bheader=fits.getheader(bflatfiles[0])
    gheader=fits.getheader(gflatfiles[0])
    rheader=fits.getheader(rflatfiles[0])
    bheader['HISTORY']='Median combined'
    gheader['HISTORY']='Median combined'
    rheader['HISTORY']='Median combined'
    fits.writeto('bflat.fits', master_bflat, bheader, clobber=True)
    fits.writeto('gflat.fits', master_gflat, gheader, clobber=True)
    fits.writeto('rflat.fits', master_rflat, rheader, clobber=True)
    


    return (master_bflat, master_gflat, master_rflat)
