#from appJar import gui
import matplotlib
matplotlib.use("TkAgg")
from numpy import *
import calib4
import img_scale
import pylab
import scipy
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import get_pkg_data_filename
import alignment5
import remove_deadhot

# handle button events
def press(button):
    if button == "Quit":
        app.stop()
    else:
        in1 = app.getEntry("Objects_blue")
        in2 = app.getEntry("Objects_green")
        in3 = app.getEntry("Objects_red")
        in4 = app.getEntry("Dark")
        in5 = app.getEntry("Bias")
        in6 = app.getEntry("Flat_blue")
        in7 = app.getEntry("Flat_green")
        in8 = app.getEntry("Flat_red")
        b, g, r=calib4.calibration(in1, in2, in3, in4, in5, in6, in7, in8)
        hot_b,fixed_b = remove_deadhot.find_outlier_pixels(b/65536.0*255.0)
        hot_g,fixed_g = remove_deadhot.find_outlier_pixels(g/65536.0*255.0)
        hot_r,fixed_r = remove_deadhot.find_outlier_pixels(r/65536.0*255.0)
        newb, newg, newr=alignment5.alignment(fixed_b,fixed_g,fixed_r)
        biasfiles=[line.rstrip('\n') for line in open(in1)]
        cat=get_pkg_data_filename(biasfiles[0])
        hdu=fits.open(cat)[0]
        wcs=WCS(hdu.header)
        n1=int(hdu.header['NAXIS1'])
        n2=int(hdu.header['NAXIS2'])
        bmin,bmax=newb.mean()-2.0*newb.std(),newb.mean()+5*newb.std()
        gmin,gmax=newg.mean()-2.0*newg.std(),newg.mean()+5*newg.std()
        rmin,rmax=newr.mean()-2.0*newr.std(),newr.mean()+5*newr.std()
        img=zeros((n1,n2,3))
        img[:,:,0]=img_scale.linear(newr,scale_min=rmin,scale_max=rmax)
        img[:,:,1]=img_scale.linear(0.9*newg,scale_min=gmin,scale_max=gmax)
        img[:,:,2]=img_scale.linear(newb,scale_min=bmin,scale_max=bmax)
        fig=pylab.figure()
        pylab.clf()
        fig.add_subplot(111,projection=wcs)
        plt.imshow(img,cmap=plt.cm.viridis)
        plt.xlabel('RA')
        plt.ylabel('DEC')
        fig.set_size_inches(10, 10, forward=True)
        plt.savefig('img')
        plt.close()
# create a GUI variable called app
app = gui("Image Process", "450x800")
app.setBg('blue')
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Please input list names")
app.setLabelBg("title", "White")
app.setLabelFg("title", "Blue")


app.addLabelEntry("Objects_blue")
app.addLabelEntry("Objects_green")
app.addLabelEntry("Objects_red")
app.addLabelEntry("Dark")
app.addLabelEntry("Bias")
app.addLabelEntry("Flat_blue")
app.addLabelEntry("Flat_green")
app.addLabelEntry("Flat_red")


# link the buttons to the function called press
app.addButtons(["Run", "Quit"], press)

#app.setFocus("Username")

# start the GUI
app.go()

'''
    input1='n5719_b.lis'    #object with blue fliter list
    input2='n5719_g.lis'    #object with green fliter list
    input3='n5719_r.lis'    #object with red fliter list
    input4='alldarkssmall.list' #dark list
    input5='allbiassmall.list'  #bias list
    input6='bflat.lis'  #blue flat field list
    input7='gflat.lis'  #green flat field list
    input8='rflat.lis'  #red flat field list
'''
