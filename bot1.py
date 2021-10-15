  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#importing the socket and string and random python librarys
import socket, string,  random # will need the random for the respose prt  

#server details
SERVER = "localhost"
PORT = 6667
CHANNEL = "#channel1" 

IRCSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    IRCSocket.connect((SERVER, PORT))
    
# send the server the bots username and nickname 
def login():
    IRCSocket.send("USER Bot networkbot server :Bot\r\n".encode())
    IRCSocket.send("NICK Bot\r\n".encode())
    
# join channel channel1
def join():
    IRCSocket.send("JOIN #channel1\r\n".encode())

#Respond to ping
def ping():
    IRCSocket.send("PONG :pingisn\r\n".encode())
    print("PONGED")

def lsiten():
    #check to see if the server is pinging 
    while (True):
        buffer = IRCSocket.recv(1024)
        message = buffer.decode()

        
        if("PING :" in message):
            ping()

        #else run the respond function sending in the message
        else:
            respond(message)
            if ("!hello" in message and "PRVITMSG Bot" not in message):
                IRCSocket.send(("PRVITMSG #channel1 : hello - \r\n").encode())
                print("hello")
        
    def respond(message):


#execute the run of the bot
connect()
login()
join()
listen()

