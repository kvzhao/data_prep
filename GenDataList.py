#! /usr/bin/env python
import fnmatch
import os, sys
import os.path
import re
import numpy as np
import scipy.io as sio

includes = ['*.mat', '*.jpg'] # for files only
excludes = ['center-error.mat', 'center-error.jpg'] # for dirs and files

errfile = 'center-error'

# transform glob patterns to regular expressions
includes = r'|'.join([fnmatch.translate(x) for x in includes])
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

# path of 'clean' dataset
data_source_root = 'ALOV/alov300++_frames/imagedata/'

#data_list = 'data_list.txt'
#fd = open(data_list, 'w')
os.system("rm alov_lists/*")

print 'Starting generate the dataset list'
for root, dirs, files in os.walk('/home/kv/workspace/Trackers/Results'):
    # exclude dirs
    dirs[:] = [os.path.join(root, d) for d in dirs]
    dirs[:] = [d for d in dirs if not re.match(excludes, d)]
    # exclude/include files
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if not re.match(excludes, f)]
    files = [f for f in files if re.match(includes, f)]

    # gurantee the order of files
    files.sort()
    # start parsing the file

    for idx, fname in enumerate(files):
        images = fname.split('/')
        tracker_type = fname.split('/')[6]
        fd = open('alov_lists/data_list_' + tracker_type + '.txt', 'a+')
        if errfile + '.mat' in images or errfile + '.jpg' in images:
            continue
        mat = sio.loadmat('/'.join(images[:-1]) + '/center-error.mat')
        score = np.array(mat['error'][0,1:])
        label = np.rint(1000 * score[idx])
        label = np.uint32(label)
        image_path = data_source_root + '/'.join(images[8:])
        # for debug 
        # print 'index', idx, ' in ', fname, str(score[idx])

        #fd.write(image_path + ' ' + str(score[idx]) + ' ' + tracker_type + '\n')
        fd.write(image_path + ' ' + str(label) + '\n')
