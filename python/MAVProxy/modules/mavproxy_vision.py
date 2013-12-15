import threading
from pykalman import KalmanFilter
import time
import libmain_py as vision
from numpy import ma

mpstate = None

class Tracker:
    def __init__(self,alpha=.5):
        self.mean = [0,0,0]
        self.cov = None
        self.kf = KalmanFilter(initial_state_mean=self.mean,n_dim_obs=3)

	self.raw_x = 0
	self.raw_y = 0
	self.raw_area = 0

        means,c = self.kf.filter([self.mean,self.mean])
        self.mean = means[-1]
        self.cov = c[-1]
	self.mode = 0

        self.fail_counter = 0
        self.fail_threshold = 20

    def set_mode(self,m):
	if m != self.mode:
	    vision.log_string("MODE: " + str(m) + "\n")
	self.mode = m

    def register_reading(self,x,y,area):
        if x == -2:
            x = ma.masked
            self.fail_counter += 1
        else:
            self.fail_counter = 0
        self.mean,self.cov = self.kf.filter_update(self.mean,self.cov,[x,y,area])

    def update(self):
	c = vision.process_frame()
	self.raw_x = c.y*2
	self.register_reading(c.y*2,0,c.area)
        self.send_update()

    def x(self):
        return self.mean[0]

    def y(self):
        return self.mean[1]

    def area(self):
        return self.mean[2]

    def __repr__(self):
        return str(self.raw_x) + ", " + str(self.y()) + ", " + str(self.area())

    def send_update(self):
        print self
	x_to_send = self.raw_x
	if x_to_send == -2:
		x_to_send = self.x()
	vision.log_string("SENDING VALUE: " + str(x_to_send) + "\n")
        if self.fail_counter > self.fail_threshold:
            #all middle values
            mpstate.master().track(127,127,127)
        else:
            mpstate.master().track(x_to_send,self.y(),self.area())

def init(_mpstate):
    print "STARTING"
    global mpstate
    mpstate = _mpstate

    mpstate.tracker = Tracker()
    vision.start()

    print "After start"
    mpstate.status.thread = threading.Thread(target=vision_loop)
    mpstate.status.thread.daemon = True
    mpstate.status.thread.start()

s = time.time()
def vision_loop():
    global s
    while True:
	#time.sleep(.01)
	mpstate.tracker.update()
	print "TIME_________________________________________________:",1000*(time.time()-s)
	s = time.time()

"""
def idle_task():
    #time.sleep(.5)
    #mpstate.tracker.update()
    #mpstate.tracker.send_update()
    pass
"""

def mavlink_packet(m):
    if m.get_type() == "STATUSTEXT":
	vision.log_string(m.text)
    if m.get_type() == "HEARTBEAT":
	mpstate.tracker.set_mode(m.custom_mode)

def name():
    '''return module name'''
    return "vision"

def description():
    '''return module description'''
    return "vision module"

def unload():
    '''unload module'''
    vision.stop()
