import cv2
import cv
import IPython
import numpy as np
import scipy.ndimage
import cPickle

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input_video')
parser.add_argument('output')
args = parser.parse_args()

FRAME_SKIP = 10
WINDOW_SIZE = 500

curr_frame_num = 0
box_starts = {}
box_ends = {}
def on_mouse(event, x, y, flags, params):
    window_size = (params[1], params[0])
    pos = (float(x)/window_size[0], float(y)/window_size[1])
    if event == cv.CV_EVENT_LBUTTONDOWN:
        box_starts[curr_frame_num] = pos
    elif event == cv.CV_EVENT_LBUTTONUP:
        box_ends[curr_frame_num] = pos

capture = cv2.VideoCapture(args.input_video)
while True:
    print 'Frame:', curr_frame_num
    retval, image = capture.read()
    image = cv2.cvtColor(image,cv2.cv.CV_RGB2GRAY)

    zoom_factor = WINDOW_SIZE / float(max(image.shape[:2]))
    image = scipy.ndimage.interpolation.zoom(image, zoom_factor)

    cv2.namedWindow('frame')
    cv.SetMouseCallback('frame', on_mouse, image.shape)
    cv2.imshow('frame', image)

    key = cv2.waitKey(0)
    if key == 27: # esc
      break

    curr_frame_num += 1

    for _ in range(FRAME_SKIP):
      capture.read()
      curr_frame_num += 1

# write output
print box_starts
print box_ends

boxes = {}
for i in box_starts:
  boxes[i] = box_starts[i] + box_ends[i]

with open(args.output, 'w') as f:
  cPickle.dump(boxes, f)
