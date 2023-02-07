
import os
import cv2
import numpy as np
from tqdm import tqdm


input_video_path = '../output_video.avi'
save_path = '../outputs/narrow_output'
remove_ends = False

inputvidcap = cv2.VideoCapture(input_video_path)


frames = int(inputvidcap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(inputvidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(inputvidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 1 #int(inputvidcap.get(cv2.CAP_PROP_FPS))# // 3
if remove_ends:
    _, input_img = inputvidcap.read()
    frames -= 2

# Read the first frame
for i in tqdm(range(frames)):
    _, input_img = inputvidcap.read()
    frame_number = str(i).zfill(4)
    path = os.path.join(save_path, f'Frame{frame_number}.png')
    cv2.imwrite(path, input_img)




