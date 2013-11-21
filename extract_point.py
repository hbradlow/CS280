import cv2
import numpy as np
import IPython

capture = cv2.VideoCapture("data/IMG_0776.MOV")
if not capture.isOpened():
    exit()
cv2.namedWindow("Main")
while True:
    rval, img = capture.read()
    width = img.shape[1]

    img = cv2.cvtColor(img,cv2.cv.CV_BGR2YCrCb)
    y,u,v = cv2.split(img)
    f = cv2.divide(cv2.add(u,v),2)
    fmin,fmax,minloc,maxloc = cv2.minMaxLoc(f)
    f = cv2.add(f,-fmin)
    f = cv2.divide(f,(fmax-fmin)/255)

    min,f = cv2.threshold(f,200,255,cv2.THRESH_BINARY_INV)

    points = np.transpose(np.nonzero(f))

    print points/float(width)

    cv2.imshow("Main",f)
    key = cv2.waitKey(20)
