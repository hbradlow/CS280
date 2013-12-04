import threading
from pykalman import KalmanFilter
import time
import libmain_py as vision

mpstate = None

class Tracker:
    def __init__(self,alpha=.5):
	self.mean = [0,0,0]
	self.cov = None
	self.kf = KalmanFilter(initial_state_mean=self.mean,n_dim_obs=3)

	means,c = self.kf.filter([self.mean,self.mean])
	self.mean = means[-1]
	self.cov = c[-1]

    def register_reading(self,x,y,area):
	self.mean,self.cov = self.kf.filter_update(self.mean,self.cov,[x,y,area])
    def update(self):
	x = vision.process_frame()
	self.register_reading(x,0,0)
        self.send_update()
    def x(self):
	return self.mean[0]
    def y(self):
	return self.mean[1]
    def area(self):
	return self.mean[2]
    def __repr__(self):
	return str(self.x()) + ", " + str(self.y()) + ", " + str(self.area())
    def send_update(self):
	print self
        mpstate.master().track(self.x(),self.y(),self.area())

def init(_mpstate):
    global mpstate
    mpstate = _mpstate

    mpstate.tracker = Tracker()
    vision.start()

    vision_thread = threading.Thread(target=vision_loop)
    vision_thread.daemon = True
    vision_thread.start()

def vision_loop():
    while True:
	time.sleep(.1)
        mpstate.tracker.update()

def mavlink_packet(m):
    pass

def name():
    '''return module name'''
    return "vision"

def description():
    '''return module description'''
    return "vision module"

def unload():
    '''unload module'''
    vision.stop()
