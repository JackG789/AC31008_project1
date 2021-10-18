import socket
import threading

HOST = "10.0.42.17"
PORT = 6667

s = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
s.bind(HOST, PORT)
print("Listening on port 6667")

def ListenforConnections(s):
    s.listen()
    while True:
        conn, addr = s.accept()
        print(f"{addr} connected")