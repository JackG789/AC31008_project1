import socket
import threading

HOST = "127.0.0.1"
PORT = 6667

nickname = input("Enter a nickname: ")

user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user.connect((HOST,PORT))



def receiveFromServer():
    while True:
        try:
            msg = user.recv(1024).decode('utf-8')
            if msg == "NICK":
                user.send(nickname.encode('utf-8'))
            else:
                print(msg)
        except:
            print("Something went wrong")
            user.close()
            break


r_thread = threading.Thread(target=receiveFromServer)
r_thread.start()

def sendToServer():
    while True:
        msg = f'{nickname}: {input("")}'
        user.send(msg.encode('utf-8'))



s_thread = threading.Thread(target=sendToServer)
s_thread.start()



