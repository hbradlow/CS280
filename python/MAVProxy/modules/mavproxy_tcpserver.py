from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

mpstate = None

class IphoneStream(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print "New client: " + str(self)
 
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print "Connection lost with:" + str(self)

    def dataReceived(self, data):
        a = data.split(':')
        if len(a) > 1:
            command = a[0]
            content = a[1]
 
            msg = ""
            if command == "msg":
                msg = "Message: " + content
                print msg
 
            for c in self.factory.clients:
                c.message(msg)

    def message(self, message):
        self.transport.write(message + '\n')                

def start_server():
    factory = Factory()
    factory.protocol = IphoneStream
    factory.clients = []
    reactor.listenTCP(8888, factory)
    print "Iphone Stream server started"
    reactor.run()

def init(_mpstate):
    global mpstate
    mpstate = _mpstate

    mpstate.status.thread = threading.Thread(target=start_server)
    mpstate.status.thread.daemon = True
    mpstate.status.thread.start()

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
