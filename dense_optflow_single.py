#! /usr/bin/env python
import cv2
import numpy as np

# PATH DEF
project_root = '/home/kv/research/trackers_ranking/'
data_source_root = 'dataset/ALOV/alov300++_frames/imagedata/'
# target frame and reference
tar_path = project_root + data_source_root + '01-Light/01-Light_video00001/00000012.jpg'
ref_path = project_root + data_source_root + '01-Light/01-Light_video00001/00000021.jpg'

tar_frame = cv2.imread(tar_path)
ref_frame = cv2.imread(ref_path)

prvs = cv2.cvtColor(tar_frame, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(tar_frame)
hsv[...,1] = 255

next = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)

flow = cv2.calcOpticalFlowFarneback(prvs,next, 0.5, 3, 15, 3, 5, 1.2, 0)
mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
hsv[...,0] = ang*180/np.pi/2
hsv[...,2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

cv2.imwrite('opticalhsv.png',rgb)

