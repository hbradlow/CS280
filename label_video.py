import cv2
import cv
import IPython
import numpy as np
import scipy.ndimage
import cPickle
import collections
import config
import utils

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input_video')
parser.add_argument('output')
args = parser.parse_args()

FRAME_SKIP = 10

curr_frame_num = 0
data = collections.defaultdict(dict)
def on_mouse(event, x, y, flags, params):
    image = params
    #window_size = (image.shape[1], image.shape[0])
    #pos = (float(x)/window_size[0], float(y)/window_size[1])
    pos = (x, y)
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print pos
        data[curr_frame_num]['start'] = pos
    elif event == cv.CV_EVENT_LBUTTONUP:
        print pos
        start, end = data[curr_frame_num]['start'], pos
        if end[0] - start[0] < 10:
          end[0] = 10
        if end[1] - start[1] < 10:
          end[1] = 10
        data[curr_frame_num]['end'] = end
        data[curr_frame_num]['full_img'] = image
        data[curr_frame_num]['box_img'] = image[start[1]:end[1], start[0]:end[0]]

capture = cv2.VideoCapture(args.input_video)
while True:
    print 'Frame:', curr_frame_num
    retval, image = capture.read()
    image = utils.canonicalize_image(image)

    cv2.namedWindow('frame')
    cv.SetMouseCallback('frame', on_mouse, image)
    cv2.imshow('frame', image)

    key = cv2.waitKey(0)
    if key == 27: # esc
      break

    curr_frame_num += 1

    for _ in range(FRAME_SKIP):
      capture.read()
      curr_frame_num += 1

# now make a training set

#import sklearn
#import sklearn.feature_extraction
all_patches = []
POS_LABEL = 1
NEG_LABEL = -1
for k in data:
  #positive_patches = sklearn.feature_extraction.image.extract_patches_2d(data[k]['box_img'], (config.PATCH_SIZE, config.PATCH_SIZE))
  #for p in positive_patches:
  #  all_patches.append((p, POS_LABEL))
  all_patches.append((utils.rect_to_patch(data[k]['box_img']), POS_LABEL))

  full_img = data[k]['full_img']
  start, end = data[k]['start'], data[k]['end']
  for _ in range(config.NEG_EXAMPLES_PER_POSITIVE):
    while True:
      a = np.random.randint(0, full_img.shape[1]-config.PATCH_SIZE)
      b = np.random.randint(0, full_img.shape[0]-config.PATCH_SIZE)
      if a > end[0] or b > end[1] or a+config.PATCH_SIZE < start[0] or b+config.PATCH_SIZE < start[1]:
        if b+config.PATCH_SIZE < image.shape[0] and a+config.PATCH_SIZE < image.shape[1]:
          p = image[b:b+config.PATCH_SIZE,a:a+config.PATCH_SIZE]
          all_patches.append((utils.rect_to_patch(p), NEG_LABEL))
          break

data['all_patches'] = all_patches

# write output
print 'got %d frames' % len(data)
with open(args.output, 'w') as f:
  cPickle.dump(data, f)

