#! /usr/bin/env python

import os, sys
import numpy as np
import matplotlib.pyplot as plt

log_name = 'cError.log'
data_path = 'error-data/'

for root, dirs, files, in os.walk(data_path):
    files.sort()
for fname in files:
    flist = fname.split('_')
    T = flist[0]
    A = flist[1]
    V = flist[2]
    if A == 'Light':
        error = np.genfromtxt(data_path + fname, delimiter=',')
