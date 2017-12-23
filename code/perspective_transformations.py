import cv2
import pickle
import numpy as np

def draw_lines(img, lines, color=[255, 0, 0], thickness=4):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    for line in lines:
#        print(line)
        cv2.line(img, line[0], line[1], color, thickness)
    return img

            

#%%

def read_camera_matrices(pickle_filepath):
    c = pickle.load(open(pickle_filepath, 'rb'))

    dist, mtx = c['dist'], c['mtx']
    return mtx, dist



#%%
# Define a function that takes an image, number of x and y points, 
# camera matrix and distortion coefficients
def perspective_transformation(img, src, dst, M, mtx, dist):
    # Use the OpenCV undistort() function to remove distortion
    undist = img 
    warped = cv2.warpPerspective(undist, M, img.shape[::-1][1:3], flags=cv2.INTER_LINEAR)


    return warped

