import os
import cv2
import numpy as np
from tqdm import tqdm

image_folder = '/data/2020-NavyRollingShutter/processed/Collect1_Narrow/Mitigated'
video_name = './small_narrow_mitigated.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images = sorted(images)

#width = 1408
#height = 792
width = 640
height = 480

video = cv2.VideoWriter(video_name, 0, 15, (width,height))

for image in tqdm(images):
    image = cv2.imread(os.path.join(image_folder, image))
    image = cv2.resize(image, (width, height))
    video.write(image)

cv2.destroyAllWindows()
video.release()