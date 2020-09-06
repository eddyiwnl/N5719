import img_scale
import alignment5
from numpy import *
import matplotlib.pyplot as plt

newb, newg, newr = alignment5.alignment(b,g,r)
bmin, bmax = newb.mean()-2.0*newb.std(),newb.mean()+10*newb.std()
gmin, gmax = newb.mean()-2.0*newg.std(),newg.mean()+10*newg.std()
rmin, rmax = newb.mean()-2.0*newr.std(),newr.mean()+10*newr.std()
Img = zeros((2048,2048,3))
img[:,:,2]=img_scale.linear(newb,scale_min=bmin,scale_max=bmax)
img[:,:,1]=img_scale.linear(newg,scale_min=gmin,scale_max=gmax)
img[:,:,0]=img_scale.linear(newr,scale_min=rmin,scale_max=rmax)
plt.imshow(img,cmap=plt.cm.viridis) #show the final RGB image
plt.show
