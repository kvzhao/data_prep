#! /usr/bin/env python
import fnmatch
import os, sys
import os.path
import re
import cv2
import numpy as np
import scipy.io as sio

from matplotlib import pyplot as plt

includes = ['*.mat', '*.jpg'] # for files only
excludes = ['center-error.mat', 'center-error.jpg'] # for dirs and files

# transform glob patterns to regular expressions
includes = r'|'.join([fnmatch.translate(x) for x in includes])
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

# path of 'clean' dataset
project_root = '/home/kv/research/trackers_ranking/'
data_source_root = project_root + 'dataset/ALOV/alov300++_frames/imagedata/'

tracked_result_path = project_root + 'dataset/ALOV_Results/'
optflow_result_path = project_root + 'dataset/ALOV_Optical/'

#print 'Trackers\tAttribute\tVideo\tMeanError\tSTD'
print 'Walk through the results tree'
for root, dirs, files in os.walk(tracked_result_path):
    # exclude dirs
    dirs[:] = [os.path.join(root, d) for d in dirs]
    dirs[:] = [d for d in dirs if not re.match(excludes, d)]
    # exclude/include files
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if not re.match(excludes, f)]
    files = [f for f in files if re.match(includes, f)]

    files.sort()
    dirs.sort()

    # go back to list find fn and center-error?
    for idx, img_path in enumerate(files):
        img_path_list = img_path.split('/')
        #print image_path_list, 'len = ', len(image_path_list)
        tracker_type = img_path_list[7]
        saving_dir = optflow_result_path + tracker_type
        try:
            os.stat(saving_dir)
        except:
            os.mkdir(saving_dir)
        fd = open(saving_dir + '/data_list_all_attr.txt', 'a+')
        if len(img_path_list) == 12:
            if img_path_list[-1].split('.')[0] == 'center-error':
                continue
            # find clean frame from source, make target and reference pair
            if (idx == 0):
                tar_img_path = data_source_root +('/').join(img_path_list[-3:])
                ref_img_path = data_source_root +('/').join(img_path_list[-3:-1]) + '/00000001.jpg'
            else :
                tar_img_path = data_source_root +('/').join(img_path_list[-3:])
                prvs_list = files[idx-1].split('/')
                ref_img_path = data_source_root +('/').join(prvs_list[-3:-1]) + '/' + prvs_list[-1]
            # Load center-error from mat
            mat = sio.loadmat('/'.join(img_path_list[:-1]) + '/center-error.mat')
            center_error = np.array(mat['error'][0,1:])[idx]
            # compute dense optical flow
            tar_frame = cv2.imread(tar_img_path)
            prvs = cv2.cvtColor(tar_frame, cv2.COLOR_BGR2GRAY)
            ref_frame = cv2.imread(ref_img_path)
            nxt = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)
            hsv = np.zeros_like(tar_frame)
            hsv[...,1] = 255
            flow = cv2.calcOpticalFlowFarneback(prvs,nxt, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
            hsv[...,0] = ang*180/np.pi/2
            hsv[...,2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

            rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
            new_name = 'optflow_' + img_path_list[-3].split('-')[1] + '_'+ img_path_list[-1].split('.')[0]
            print 'create the optical flow image', new_name
            try:
                os.stat(saving_dir)
            except:
                os.mkdir(saving_dir)
            img_saving_path = saving_dir + '/' + new_name + '.jpg'
            fd.write(img_saving_path + ' ' + str(center_error) + '\n')
            cv2.imwrite(img_saving_path, rgb)

