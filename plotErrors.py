#! /usr/bin/env python

import os, sys
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

data_path = 'error-data/'
fig_path = 'error-figs/'
os.system("rm -rf error-figs/*")

# global list in order, Trackers/Attributes/Videos
T, A, V = [], [], []
# dict
D = {}

def load_err_fromtxt(t, a, v):
    array_path = data_path + '_'.join([t,a,v]) + '.out'
    fn_path = array_path.replace('video','fn')
    error = np.genfromtxt(array_path)
    fno = np.genfromtxt(fn_path)
    return error, fno

# walk the assigned directory
for root, dirs, files, in os.walk(data_path):
    files.sort()
# parsing all files name
for fname in files:
    flist = fname.split('_')
    T.append(flist[0])
    A.append(flist[1])
    key = flist[0]+flist[1]
    if 'video' in flist[2]:
        D.setdefault(key, []).append(flist[2].rstrip('.out'))
    V.append(flist[2].rstrip('.out'))
# trackers and attributes
trackers = set(T)
attributes = set(A)

# more like cpp style generating folders
for a in attributes:
    os.mkdir(fig_path + a)

# general purposes data parsing done
# --------------------------------------------------------

# plot all trackers w.r.t different attributes and videos
for attr in attributes:
    for t in trackers:
        video_list =  D[t+attr]
        for v in video_list:
            labels = []
            plt.clf()
            for t2 in trackers:
                [err, f_no] = load_err_fromtxt(t2,attr,v)
                # BAD TRICKS
                if len(err) != len(f_no):
                    err = err[1:]
                plt.plot(f_no, err)
                labels.append(t2)
                plt.legend(labels, ncol=4, loc='upper center', bbox_to_anchor=[0.5, 1.1], 
                    columnspacing=1.0, labelspacing=0.0,
                    handletextpad=0.0, handlelength=1.5,
                    fancybox=True, shadow=True)
                #plt.savefig(fig_path + '_'.join([attr,v])+'.jpg')
                # save diff dirs
                plt.savefig(fig_path+attr+'/'+v+'.jpg')
