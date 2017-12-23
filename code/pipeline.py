# Import libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle
from image_transformations import *
from find_lanes_pipeline import *
from perspective_transformations import *
from class_line import Line

#%% Camera calibration importing the matrices
mtx, dist = read_camera_matrices('wide_dist_pickle.p')
src = np.float32([(200, 720),(600, 450), (700, 450),  (1100, 720)])
dst = np.float32([(350, 720), (380, 0), (1060,0), (960,720)])

M = cv2.getPerspectiveTransform(src, dst)
Minv = cv2.getPerspectiveTransform(dst, src)


#%% Definition of left and right lines
Left_line = Line()
Right_line = Line()


#%% 
def line_checks(Line,line_fit):
    '''
    Input: Line class and the fitting line
    Output: Updates the line class
    
    Operation: When the function is called, the lane fit line is checked if it satisfies several conditions.
    First, if it is empty, it means that the find line algorithm was not able to identify a line for this frame and the average of the 
    previous frames is provided. The line detected flag is false and for the next frame the find_line_blind variation of the function is 
    called, which will detect the line from scratch.
    If the fit line is valid, again that line is checked against previous frames and has to be with 10% range. Otherwise the results is 
    considered wrong and again the average of previous frames is provided as the fit line.
    When the condition of 10% is satisfied, the current line finding is accepted the it is added to a queue of recent frames, of depth 3 
    and the average is the output. The averaging is performaned to smooth the output.
    
    '''
    # Initializations
    Line.detected = False
    frames_depth = 3
    if line_fit != []:
        if Line.best_fit == None:
            Line.best_fit = line_fit
            
        # If line is very different from average drop it
        drop_condition = (np.abs(line_fit - Line.best_fit) > 0.1*Line.best_fit)
 
        # Check that line is within 10% of previous frame
        if not drop_condition.all():
            Line.current_fit = line_fit
            Line.recent_xfitted.append(line_fit)
            Line.detected = True
    
        
    if len(Line.recent_xfitted) > frames_depth:
        Line.recent_xfitted.pop(0)
    Line.best_fit = np.average(Line.recent_xfitted,axis=0)
    return Line
#%% Performs undistortion, persective transformantion, line searching, curvature finding
def pipeline(image):
    '''
    Left and Right Lines are searched for each frame
    For the first frame, or then a frame does not return a line, the blind search (find_lines_blind) is performed which is using 
    the histogram meathod to identify lines without any initial conditions
    If a frame has been found, the find_line function is using the found lines, to search the new ones for the next frame.
    
    Curvature and shifting are calculated and added to the frame. 
    
    '''
    # Image transformation
    global Left_line, Right_line
    
    undist = cv2.undistort(image, mtx, dist, None, mtx)
    warped = perspective_transformation(undist, src, dst, M, mtx, dist)    
    img_binary = color_transformation_pipeline(warped)
    
    if (Left_line.detected == False | Right_line.detected == False):
        img_lane_lines, left_fit, right_fit = find_lines_blind(img_binary)
    else:
        img_lane_lines, left_fit, right_fit = find_lines(img_binary, Left_line.best_fit, Right_line.best_fit ) 
        
    Left_line = line_checks(Left_line,left_fit)
    Right_line = line_checks(Right_line,right_fit)

    curvature, shft = find_curvature(img_binary, Left_line.best_fit, Right_line.best_fit)
    out_image = plot_lane_lines(img_binary, undist, Left_line.best_fit, Right_line.best_fit, Minv, curvature, shft)

    return out_image

#%%
from moviepy.editor import VideoFileClip

video_output = '../video_lane.mp4'
clip1 = VideoFileClip("../project_video.mp4")
video_clip = clip1.fl_image(pipeline)
video_clip.write_videofile(video_output, audio=False)

