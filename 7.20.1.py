import os
import matplotlib.pyplot as plt
import master_dark1
import master_bias2
import master_flat3
import calib4
import remove_deadhot
import alignment5
import img_scale
from numpy import *

asps = []
asps2 = []
asps3 = []
asps4 = []
asps5 = []
asps6 = []
asps7 = []
asps8 = []
for root,dirs,files in os.walk(r'F:\Python practice'):
    for file in files:
        #something
        if file.endswith('dm.fit'):
           asps.append(file)
           with open(file) as f:
                lines = f.readlines()
                lines = [l for l in lines if "ROW" in l]
                with open ("dark.lis","w")as f1:
                    for i in range(0,len(asps)):
                        f1.writelines(asps[i] + "\n")
                    f1.writelines(lines)
        if file.endswith('bm.fit'):
            asps2.append(file)
            with open(file) as f:
                lines = f.readlines()
                lines = [l for l in lines if "ROW" in l]
                with open("bias.lis", "w")as f1:
                    for i in range(0, len(asps2)):
                        f1.writelines(asps2[i] + "\n")
                    f1.writelines(lines)
        if file.endswith('bff.fit'):
            asps3.append(file)
            with open(file) as f:
                lines = f.readlines()
                lines = [l for l in lines if "ROW" in l]
                with open("bflat.lis", "w")as f1:
                    for i in range(0, len(asps3)):
                        f1.writelines(asps3[i] + "\n")
                    f1.writelines(lines)
        if file.endswith('gff.fit'):
            asps4.append(file)
            with open(file) as f:
                lines = f.readlines()
                lines = [l for l in lines if "ROW" in l]
                with open("gflat.lis", "w")as f1:
                    for i in range(0, len(asps4)):
                        f1.writelines(asps4[i] + "\n")
                    f1.writelines(lines)
        if file.endswith('rff.fit'):
            asps5.append(file)
            with open(file) as f:
                lines = f.readlines()
                lines = [l for l in lines if "ROW" in l]
                with open("rflat.lis", "w")as f1:
                    for i in range(0, len(asps5)):
                        f1.writelines(asps5[i] + "\n")
                    f1.writelines(lines)
        if file.endswith('Blue.fts'):
            asps6.append(file)
            with open(file) as f:
                lines = f.readlines()
                lines = [l for l in lines if "ROW" in l]
                with open("b.lis", "w")as f1:
                    for i in range(0, len(asps6)):
                        f1.writelines(asps6[i] + "\n")
                    f1.writelines(lines)
        if file.endswith('Green.fts'):
            asps7.append(file)
            with open(file) as f:
                lines = f.readlines()
                lines = [l for l in lines if "ROW" in l]
                with open("g.lis", "w")as f1:
                    for i in range(0, len(asps7)):
                        f1.writelines(asps7[i] + "\n")
                    f1.writelines(lines)
        if file.endswith('Red.fts'):
            asps8.append(file)
            with open(file) as f:
                lines = f.readlines()
                lines = [l for l in lines if "ROW" in l]
                with open("r.lis", "w")as f1:
                    for i in range(0, len(asps8)):
                        f1.writelines(asps8[i] + "\n")
                    f1.writelines(lines)

dark,t = master_dark1.master_dark('dark.lis')
#plt.imshow(dark, cmap='gray')
#plt.show()
bias = master_bias2.master_bias('bias.lis')
#plt.imshow(bias, cmap='gray')
#plt.show()
bflat,gflat,rflat=\
master_flat3.master_flat('bflat.lis','gflat.lis','rflat.lis')
#plt.imshow(bflat, cmap='gray')
#plt.show()
master_b,master_g,master_r=\
calib4.calibration('b.lis','g.lis','r.lis','dark.lis','bias.lis','bflat.lis','gflat.lis','rflat.lis')
#plt.imshow(master_b, cmap='gray')
#plt.show()
hot_pixels_b,b = remove_deadhot.find_outlier_pixels(master_b)
hot_pixels_g,g=remove_deadhot.find_outlier_pixels(master_g)
hot_pixels_r,r=remove_deadhot.find_outlier_pixels(master_r)
newb,newg,newr=alignment5.alignment(b,g,r)
bmin, bmax = newb.mean()-2.0*newb.std(),newb.mean()+20*newb.std()
gmin, gmax = newg.mean()-2.0*newg.std(),newg.mean()+20*newg.std()
rmin, rmax = newr.mean()-2.0*newr.std(),newr.mean()+20*newr.std()
img = zeros((2048,2048,3))
img[:,:,2]=img_scale.linear(newb,scale_min=bmin,scale_max=bmax)
img[:,:,1]=img_scale.linear(newg,scale_min=gmin,scale_max=gmax)
img[:,:,0]=img_scale.linear(newr,scale_min=rmin,scale_max=rmax)
plt.imshow(img,cmap=plt.cm.viridis) #show the final RGB image
plt.text(1600,2000,"Edward Du",color = "red")
plt.show()

