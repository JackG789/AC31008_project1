import socket

#clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clientSocket.connect((SERVER, PORT))

UserName = raw_input('Please Enter your Username: ')
RealName = raw_input('Please Enter your Realname: ')

clientSocket.send(Username.encode())
clientSocket.send(RealName.encode())