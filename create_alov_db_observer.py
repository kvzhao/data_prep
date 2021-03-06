# !/usr/bin/env python

from subprocess import call, check_call
import re
import os, sys

# dir_paths
project_path = '/home/kv/research/trackers_ranking/'
root_path = project_path + '/caffe_for_trackerRank/'
db_save_path = root_path + 'data/alov_sameObserver/'
lists_path = project_path + 'dataset/data_prep/alov_lists/'

# file_names
db_name_prefix = 'alov_dataset_observer_'

# commandline options
backend_flag = '-backend lmdb'
shuffle_flag = '-shuffle=true'
width_flag  = '-resize_height=225'
height_flag = '-resize_width=225'

# program
image_converter = root_path + 'build/tools/convert_imageset.bin'
image_mean_computer = root_path + 'build/tools/compute_image_mean.bin'

# delete the existing files
#call(['rm', '-rf', db_save_path + db_name_prefix + '*'])
os.system('rm -rf ' + db_save_path + db_name_prefix + '*')

for root, dirs, files in os.walk(lists_path):
    for fname in files:
        tracker_type = re.split(r'[_.]+', fname)[-2]
        datum_list_path = lists_path + fname 
        db_filename = db_save_path + db_name_prefix + tracker_type
        call([image_converter, height_flag, width_flag, shuffle_flag, project_path, datum_list_path, db_filename])
        call([image_mean_computer, db_filename, db_filename +'/mean.binaryproto'])
