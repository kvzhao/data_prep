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

data_source_root = '/home/kv/workspace/Trackers/ALOV'

for root, dirs, files in os.walk('/home/kv/workspace/Trackers'):
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
        print idx
        images = fname.split('/')
        if errfile + '.mat' in images or errfile + '.jpg' in images:
            continue
        mat = sio.loadmat('/'.join(images[:-1]) + '/center-error.mat')
        score = np.array(mat['error'][0,1:])
        print data_source_root + '/'.join(images[7:])
        # is this right?
        print score[idx]
