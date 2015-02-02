#! /usr/bin/env python

import os, sys
import re
import fnmatch
import numpy as np
import scipy.io as sio

# root_dir = sys.argv[1]
# assign root director
result_dir = 'Results/'
result_dir = 'Results/CSK/'
print result_dir

fd = open('data_list', 'w')

# prevent note.txt file
excludes = ['*.txt']
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

for root, dirs, files in os.walk(result_dir):
    dirs = [os.path.join(root, d) for d in dirs]
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if not re.match(excludes, f)]

    # avoid empty list and sort the list with file name
    if files:
        files.sort()
    for fname in files:
        images = fname.split('/')
        if 'center-error.jpg' in images:
            images.remove('center-error.jpg')
        if 'center-error.mat' in images:
            images.remove('center-error.mat')
            mat = sio.loadmat(root + '/center-error.mat')
            fd.write('/'.join(images) + '\n')

