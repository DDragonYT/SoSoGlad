import struct
import threading
import socket

# Test client for hosting the MMORPG aspects on a standalone app

class Client():
    def __init__(self, host="127.0.0.1", port = 25564):
        self.host = host
        self.port = port
        self.socket = None

    def run_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.connect((self.host, self.port))
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            s.settimeout(1)
            print("Connected",s)
            self.socket = s
    
    def run(self):
        threading.Thread(target=self.run_listener).start()
        while True:
            # self.update()
            pass

Client().run()