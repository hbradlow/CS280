import serial
import time

ser = serial.Serial('/dev/ttyACM0',115200)

while True:
	ser.write(str(140))
	ser.flush()
	print "HERE"
	print ser.read()
	time.sleep(1)

ser.close()
