import libmain_py as vision
import time
import sys

vision.start()

counter = 0
while True:
	counter += 1
	s = time.time()
	c = vision.process_frame()
	sys.stdout.write(str(c.area) + " " + str(c.x) + " " + str(c.y) + " Time: " + str(1000*(time.time()-s)) + "\r")
	sys.stdout.flush()
