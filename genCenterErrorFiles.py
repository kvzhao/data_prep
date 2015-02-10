#! /usr/bin/env python
import fnmatch
import os, sys
import os.path
import re
import numpy as np
import scipy.io as sio

from matplotlib import pyplot as plt

includes = ['*.mat', '*.jpg'] # for files only
excludes = ['center-error.mat', 'center-error.jpg'] # for dirs and files

# transform glob patterns to regular expressions
includes = r'|'.join([fnmatch.translate(x) for x in includes])
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

# path of 'clean' dataset
data_source_root = 'ALOV/alov300++_frames/imagedata/'
errfile = 'center-error'
save_path = 'error-data/'

os.system("rm error-data/*")

#print 'Trackers\tAttribute\tVideo\tMeanError\tSTD'
for root, dirs, files in os.walk('/home/kv/workspace/trackers_ranking/Results'):
    # exclude dirs
    dirs[:] = [os.path.join(root, d) for d in dirs]
    dirs[:] = [d for d in dirs if not re.match(excludes, d)]
    # exclude/include files
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if not re.match(excludes, f)]
    files = [f for f in files if re.match(includes, f)]

    files.sort()
    dirs.sort()
    
    for idx, dir_path in enumerate(dirs):
        dir_list = dir_path.split('/')
        if len(dir_list) == 10:
            # name extraction
            tracker_type = dir_list[6]
            attribute      = dir_list[8].split('-')[1]
            video_name   = dir_list[9].split('_')[1]
            #fd = open(save_path + tracker_type + '_' + attribute + '_' + video_name + '.txt', 'a+')
            mat = sio.loadmat(dir_path+ '/center-error.mat')
            # datum extraction
            center_error = np.array(mat['error'][0,0:])
            fn = np.array(mat['f_no'][0,0:])
            if len(center_error) != len(fn):
                center_error = np.array(mat['error'][0,1:])
            #plt.plot(fn, center_error)
            mean = np.mean(center_error)
            std = np.std(center_error)
            print tracker_type, attribute, video_name, str(mean), str(std)
            #fd.write(center_error)
            np.savetxt(save_path + tracker_type + '_' + attribute + '_' + video_name + '.out', center_error, delimiter=',')
            np.savetxt(save_path + tracker_type + '_' + attribute + '_' + video_name.replace('video', 'fn') + '.out', fn, delimiter=',')
    #plt.show()
