#!/usr/bin/python
from __future__ import print_function
import pyoptics.tfsdata as tfs
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.constants
import math
import sys
import tune_diagram
import footprint

if sys.version_info[0] < 3:
    import NAFFlib2 as NAFFlib
else:
    import NAFFlib

plt.style.use('kostas')

sig = 1.157751566e-05
n = 15

xy = footprint.initial_xy_polar(sig,n*sig,n,0.01*np.pi,np.pi*(1/2.-0.01),10)
trackdir = 'tracks/'
if not os.path.exists(trackdir):
    os.makedirs(trackdir)
temptxt = open('temp.txt','w')
temptxt.write('call, file="toy.seq";\n')
temptxt.write('Beam, particle=proton, npart:=1.e11, energy = 6500.0;\n')
temptxt.write('use, sequence=toymachine;\n')
temptxt.write('track, file={0}/track;\n'.format(trackdir.strip('/')))
for x in xy:
    for y in x:
        temptxt.write('start, x={0:.10f}, y={1:.10f}, px=0, py=0, t=0,pt=1.e-4;\n'.format(y[0],y[1]))
temptxt.write('run, turns = 100;\n')
temptxt.write('endtrack;\n')
temptxt.write('stop;\n')
temptxt.close()

os.system('madx < temp.txt')

fig1 = plt.figure(1,figsize=(20,10))
ax1=plt.subplot(1,2,1)
for order in [1,2,3]:
    TD = tune_diagram.ResonanceLines(0,0,order,1)
    TD.plot_resonance(fig1)
ax1.plot([0.29],[0.31],'r.',markersize=20)
ax2=plt.subplot(1,2,2)


Q_arr = np.empty_like(xy)
k=0
for q1 in Q_arr:
    for q2 in q1:
        B=tfs.open(trackdir+'track.obs0001.p{0:04d}'.format(k+1))
        Bx = B['x'][np.isfinite(B['x'])]
        By = B['y'][np.isfinite(B['y'])]
        qx1 = NAFFlib.get_tune(Bx);
        qy1 = NAFFlib.get_tune(By);
        #print('{0:d}  {1:.3f}  {2:.3f} '.format(k, qx1, qy1))
        q2[0]=qx1
        q2[1]=qy1
        k+=1

ax1.plot([0.29],[0.31],'r.',markersize=20)
ax2.plot(xy[:,:,0],xy[:,:,1],'b.')
footprint.draw_footprint(Q_arr, fig1, 0)
footprint.draw_footprint(xy, fig1, 1)
ax1.set_xlabel('$Q_x$')
ax1.set_ylabel('$Q_y$')
#ax1.set_xlim(0.25,0.30)
#ax1.set_ylim(0.28,0.315)
ax2.set_xlabel('$x$')
ax2.set_ylabel('$y$')
plt.show(False)
input()


