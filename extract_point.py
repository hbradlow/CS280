import cv2
import numpy as np
import IPython
from inference import *

capture = cv2.VideoCapture("data/IMG_0776.MOV")
if not capture.isOpened():
    exit()
cv2.namedWindow("Main")
points_list = []
index = 0
while True:
    rval, img = capture.read()
    if img is None:
        break
    height,width,channels = img.shape
    img = cv2.resize(img,(int(width/4.0),int(height/4.0)))
    height,width,channels = img.shape

    print index
    index += 1

    img = cv2.cvtColor(img,cv2.cv.CV_BGR2YCrCb)
    y,u,v = cv2.split(img)
    f = cv2.divide(cv2.add(u,v),2)
    fmin,fmax,minloc,maxloc = cv2.minMaxLoc(f)
    f = cv2.add(f,-fmin)
    f = cv2.divide(f,(fmax-fmin)/255)

    min,f = cv2.threshold(f,200,255,cv2.THRESH_BINARY_INV)

    points = np.transpose(np.nonzero(f))

    points = points/float(width)

    print "num points:",points.shape[0]
    points_list.append(points)



    tracker = Tracker(mean_x_prior=np.array([10,10]),var_x=100000, var_z=.01, noise_density=1, noise_prob=.1)
    tracker.set_observations(points)
    curr_x, x_history, obj_val_history = tracker.run_em(init_x=np.array([0,0]))
    print 'result', curr_x

    top_left = tuple((curr_x*width).astype(int)-np.array([5,5]))
    bottom_right = tuple((curr_x*width).astype(int)+np.array([5,5]))
    print top_left
    cv2.rectangle(f,top_left,bottom_right,(255,0,0),0)
    cv2.imshow("Main",f)
    key = cv2.waitKey(20)
