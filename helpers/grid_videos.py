import os
import cv2
import numpy as np
from tqdm import tqdm


input_video_path = './wide.avi'
output_video_path = '../output_video.avi'
gridded_video = './gridded_wide_newmodel_video.avi'

inputvidcap = cv2.VideoCapture(input_video_path)
outputvidcap = cv2.VideoCapture(output_video_path)


frames = int(outputvidcap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(inputvidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(inputvidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 1 #int(inputvidcap.get(cv2.CAP_PROP_FPS))# // 3
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
size = (width, height)
video = cv2.VideoWriter(gridded_video, fourcc, fps, size)

# Read the first frame
_, _ = inputvidcap.read()
n = 100
for i in tqdm(range(frames)):
    _, input_img = inputvidcap.read()
    _, output_img = outputvidcap.read()
    zero_tile = np.zeros((n,n,3))
    one_tile = np.ones((n,n,3))
    initial_checker = np.concatenate((zero_tile, one_tile), axis=0)
    initial_checker = np.concatenate((initial_checker, initial_checker[::-1, ...]), axis=1)
    new_frame = np.pad(
        initial_checker, ((0, height - (2*n)), (0, width - (2*n)), (0, 0)), mode='wrap')
    new_frame = np.where(new_frame == 1, input_img, output_img)
    w_marks = np.arange(0, width, n)
    h_marks = np.arange(0, height, n)
    new_frame[h_marks, :, :] = (0, 0, 255)
    new_frame[:, w_marks, :] = (0, 0, 255)
    try:
        video.write(new_frame)
    except:
        continue

cv2.destroyAllWindows()
video.release()

