import smbus
import time
import libmain_pi
import IPython

bus = smbus.SMBus(1)

address = 0x04

def writeNumber(value):
	bus.write_byte(address,value)
def readNumber():
	return bus.read_byte(address)

libmain_pi.init_main_pi()

while True:
	component = libmain_pi.process_frame()
	writeNumber(component.x);
	writeNumber(' ');
	writeNumber(component.y);
	writeNumber('\n');

libmain_pi.stop_main_pi();
