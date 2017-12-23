import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle
from image_transformations import *
from find_lanes_pipeline import *
from perspective_transformations import *


# Calibrate the camera importing the matrices
mtx, dist = read_camera_matrices('wide_dist_pickle.p')

#dst = np.float32([(350, 720), (380, 0), (1060,0), (960,720)])

# Original image
img_path = '../test_images/test4.jpg'
img = plt.imread(img_path)
plt.imshow(img)

#%% Undistorted image
undist = cv2.undistort(img, mtx, dist, None, mtx)
plt.imshow(undist)
plt.imsave('test4_undist.png', undist)

#%% Binary image

img_binary = color_transformation_pipeline(undist)
plt.imshow(img_binary, cmap='gray')
plt.imsave('test4_binary.png',img_binary, cmap='gray' )

#%% Setting the source points


#src = [(210, 720),(600, 450), (680, 450),  (1100, 720)]
#dst = np.float32([(350, 720), (380, 0), (1060,0), (960,720)])

src = np.float32([(200, 720),(600, 450), (700, 450),  (1100, 720)])
dst = np.float32([(350, 720),(380, 0), (1060,0), (960,720)])
M = cv2.getPerspectiveTransform(src, dst)
Minv = cv2.getPerspectiveTransform(dst, src)
undist = cv2.undistort(img, mtx, dist, None, mtx)

#lines = [[src[0],src[1]], [src[1],src[2]], [src[2],src[3]], [src[3],src[0]]]
#img_points = draw_lines(undist, lines)
#plt.imsave('image_point.png', img_points)

#plt.imshow(draw_lines(img_points, lines))

#%% Perspective transformation
src = np.float32(src)
#dst = np.float32([(350, 720), (350, 0), (800,0), (1160,720)])
undist = cv2.undistort(img, mtx, dist, None, mtx)
warped = perspective_transformation(undist, src, dst, M, mtx, dist)

plt.imshow(warped)
plt.imsave('test4_warped.png', warped)

#%%
img_binary = color_transformation_pipeline(warped)
plt.imshow(img_binary, cmap='gray')
#plt.imsave('test4_warped_binary.png',img_binary, cmap='gray' )


#%% Draw lane lines

img_lane_lines, left_fit, right_fit = find_lines_blind(img_binary)


#%%
curvature, shift = find_curvature(img_binary, left_fit, right_fit)
out_image = plot_lane_lines(img_binary, undist, left_fit, right_fit, Minv, curvature, shift)
plt.imshow(out_image)
plt.imsave('test4_final.png', out_image)
