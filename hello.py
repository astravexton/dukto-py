import getpass, socket, sys, time, threading
import netifaces as ni

class Runner(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.connected = False
        self.NETWORK_PORT = 4644
        self.BROADCAST_ADDRESSES = []
        self.IGNORE_ADDRESSES = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(("0.0.0.0", self.NETWORK_PORT))
        for interface in ni.interfaces():
            try:
                self.IGNORE_ADDRESSES.append(ni.ifaddresses(interface)[2][0]["addr"])
                self.BROADCAST_ADDRESSES.append(ni.ifaddresses(interface)[2][0]["broadcast"])
            except KeyError:
                pass

    def getSystemSignature(self):
        signature = "{} at {} running dukto-py ({})".format(
            getpass.getuser(), socket.gethostname(), sys.platform)
        return signature

    def run(self):
        self.connected = True
        self.packet = "\x01{}".format(self.getSystemSignature())
        while self.connected:
            self.send(self.packet)
            time.sleep(60)

    def stop(self):
        print(" ")
        self.send("\x03Bye Bye")
        self.connected = False
        self.s.close()

    def send(self, data):
        data = data.encode()
        for address in self.BROADCAST_ADDRESSES:
            self.s.sendto(data, (address, self.NETWORK_PORT))
            print("Sent", data, "to", address)

    def recv(self):
        recv = self.s.recvfrom(2048)
        if recv[1][0] not in self.IGNORE_ADDRESSES:
            print(">>", recv[0], "from", recv[1][0])

if __name__ == "__main__":
    sys.exit("Please run main.py")
