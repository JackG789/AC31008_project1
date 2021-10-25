import socket
import threading
import os
#initialise server details
HOST = "::1"
PORT = 6667

nickname = input("Enter a nickname: ")
#initialise socket
user = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
user.connect((HOST,PORT))
#Receive info and messages from the server
def receiveFromServer():
    while True:
        try:
            msg = user.recv(1024).decode('utf-8')

            if msg == "NICK":
                user.send(nickname.encode('utf-8'))
            elif msg == "EXIT":
                user.close()
                os._exit(1)
            else:
               print(msg)

        except:
            print("Something went wrong")
            user.close()
            break

#initialise thread
r_thread = threading.Thread(target=receiveFromServer)
r_thread.start()

#Send messages to server
def sendToServer():
    while True:
        msg = input("")
        user.send(msg.encode('utf-8'))


#initialise thread
s_thread = threading.Thread(target=sendToServer)
s_thread.start()



