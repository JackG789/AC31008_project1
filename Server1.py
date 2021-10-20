import socket
import threading

HOST = "127.0.0.1"
PORT = 6667
#socket initialistion
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
print("Listening on port 6667....")

users = []
nicknames = []

def connectUser(s):
    s.listen()
    while True:
        user, addr = s.accept()
        print(f"{str(addr)} has connected")
        
        user.send('NICK'.encode('utf-8')) #server sends keyword to client to receive nickname
        nickname = user.recv(1024).decode('utf-8') 
        nicknames.append(nickname)
        users.append(user)

        sendMessage(f'{nickname} has joined the server'.encode('utf-8'))
       
        thread = threading.Thread(target = handleClient, args =(user,))
        thread.start()

def sendMessage(msg):
    for user in users:
        user.send(msg)



def handleClient(user):
    while True:
         msg = user.recv(1024)
         sendMessage(msg)
        



connectUser(s)


