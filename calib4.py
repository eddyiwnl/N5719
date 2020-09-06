from astropy.io import fits
import matplotlib
matplotlib.use("TkAgg")
from numpy import *
import pylab
import scipy
import matplotlib.pyplot as plt
import master_flat3, master_dark1, master_bias2

def calibration(inputb, inputg, inputr, input_dark, input_bias, flat_b, flat_g, flat_r):
    bfiles=[line.rstrip('\n') for line in open(inputb)]
    gfiles=[line.rstrip('\n') for line in open(inputg)]
    rfiles=[line.rstrip('\n') for line in open(inputr)]


    bsci=[]
    gsci=[]
    rsci=[]

    for file1 in bfiles:
        bsci.append(fits.getdata('%s' % file1))
    for file2 in gfiles:
        gsci.append(fits.getdata('%s' % file2))
    for file3 in rfiles:
        rsci.append(fits.getdata('%s' % file3))
    header=fits.getheader(bfiles[0])
    exptime=header['EXPTIME']
    dark, dark_time=master_dark1.master_dark(input_dark)
    bias=master_bias2.master_bias(input_bias)
    bflat, gflat, rflat=master_flat3.master_flat(flat_b, flat_g, flat_r)


    finalb=((bsci-dark/float(dark_time)*float(exptime))/(bflat-bias))*mean(bflat-bias)
    finalg=((gsci-dark/float(dark_time)*float(exptime))/(gflat-bias))*mean(gflat-bias)
    finalr=((rsci-dark/float(dark_time)*float(exptime))/(rflat-bias))*mean(rflat-bias)

#print shape(finalb)

    master_b=median(finalb,axis=0)
    master_g=median(finalg,axis=0)
    master_r=median(finalr,axis=0)

    bheader=fits.getheader(bfiles[0])
    gheader=fits.getheader(gfiles[0])
    rheader=fits.getheader(rfiles[0])
    bheader['HISTORY']='Median combined'
    gheader['HISTORY']='Median combined'
    rheader['HISTORY']='Median combined'
    fits.writeto('object_b.fits', master_b, bheader, clobber=True)
    fits.writeto('object_g.fits', master_g, gheader, clobber=True)
    fits.writeto('object_r.fits', master_r, rheader, clobber=True)
    return (master_b, master_g, master_r)




'''
    fig=pylab.figure()

    pylab.subplot(3,1,1)
    plt.imshow(master_b,cmap='gray')
#pylab.legend(loc='upper right',prop={'size':10})
    pylab.title('N5719')

    pylab.subplot(3,1,2)
    plt.imshow(master_g,cmap='gray')
#pylab.legend(loc='upper right',prop={'size':10})

    pylab.subplot(3,1,3)
    plt.imshow(master_r,cmap='gray')
#pylab.legend(loc='upper right',prop={'size':10})

    fig.set_size_inches(4, 8, forward=True)
    pylab.savefig('N5719_3')
    pylab.close()
'''
