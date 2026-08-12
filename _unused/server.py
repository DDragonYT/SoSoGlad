import time
import struct
import threading
import socket

# Test server for hosting the MMORPG aspects on a standalone app

class Server():
    def __init__(self, host="127.0.0.1", port=25564):
        self.host = host
        self.port = port
        self.kill = False
        self.thread_count = 0
        self.players = []

    def run_listener(self, conn):
        self.thread_count += 1
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        conn.settimeout(1)
        self.thread_count -= 1

    def connection_listen_loop(self):
        self.thread_count += 1
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.bind((self.host, self.port))

            while not self.kill:
                s.settimeout(1)
                s.listen()
                try:
                    conn, addr = s.accept()
                    print("New connection",conn,addr)
                    if len(self.players) < 2:
                        self.players.append(conn)

                except socket.timeout:
                    continue
                time.sleep(0.01)

        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print("Killed")

    def run(self):
        threading.Thread(target = self.connection_listen_loop).start()
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.await_kill = True



Server().run()
