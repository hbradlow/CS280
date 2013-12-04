import smbus
import time
import libmain_pi
import time
import serial
from optparse import OptionParser
parser = OptionParser("mavproxy.py [options]")

parser.add_option("--master",dest="master", action='append', help="MAVLink master port", default=[])
parser.add_option("--baudrate", dest="baudrate", type='int',
	      help="master port baud rate", default=115200)
parser.add_option("--out",   dest="output", help="MAVLink output port",
	      action='append', default=[])
parser.add_option("--sitl", dest="sitl",  default=None, help="SITL output port")
parser.add_option("--streamrate",dest="streamrate", default=4, type='int',
	      help="MAVLink stream rate")
parser.add_option("--source-system", dest='SOURCE_SYSTEM', type='int',
	      default=255, help='MAVLink source system for this GCS')
parser.add_option("--target-system", dest='TARGET_SYSTEM', type='int',
	      default=1, help='MAVLink target master system')
parser.add_option("--target-component", dest='TARGET_COMPONENT', type='int',
	      default=1, help='MAVLink target master component')
parser.add_option("--logfile", dest="logfile", help="MAVLink master logfile",
	      default='mav.tlog')
parser.add_option("-a", "--append-log", dest="append_log", help="Append to log files",
	      action='store_true', default=False)
parser.add_option("--quadcopter", dest="quadcopter", help="use quadcopter controls",
	      action='store_true', default=False)
parser.add_option("--setup", dest="setup", help="start in setup mode",
	      action='store_true', default=False)
parser.add_option("--nodtr", dest="nodtr", help="disable DTR drop on close",
	      action='store_true', default=False)
parser.add_option("--show-errors", dest="show_errors", help="show MAVLink error packets",
	      action='store_true', default=False)
parser.add_option("--speech", dest="speech", help="use text to speach",
	      action='store_true', default=False)
parser.add_option("--num-cells", dest="num_cells", help="number of LiPo battery cells",
	      type='int', default=0)
parser.add_option("--aircraft", dest="aircraft", help="aircraft name", default=None)
parser.add_option("--cmd", dest="cmd", help="initial commands", default=None)
parser.add_option("--console", action='store_true', help="use GUI console")
parser.add_option("--map", action='store_true', help="load map module")
parser.add_option(
'--load-module',
action='append',
default=[],
help='Load the specified module. Can be used multiple times, or with a comma separated list')
parser.add_option("--mav09", action='store_true', default=False, help="Use MAVLink protocol 0.9")
parser.add_option("--auto-protocol", action='store_true', default=False, help="Auto detect MAVLink protocol version")
parser.add_option("--nowait", action='store_true', default=False, help="don't wait for HEARTBEAT on startup")
parser.add_option("--continue", dest='continue_mode', action='store_true', default=False, help="continue logs")
parser.add_option("--dialect",  default="ardupilotmega", help="MAVLink dialect")

from setup import *
(opts, args) = parser.parse_args()
setup(opts,args)
time.sleep(20)
print "Going ahead with stuff"

libmain_pi.init_main_pi()

prev = time.time()
while True:
	x = libmain_pi.process_frame()
	cmd_track([x,0,0])	
	print "X:",x,"\t\tTime:",1000*(time.time()-prev)
	prev = time.time()
	#time.sleep(1)

libmain_pi.stop_main_pi();
