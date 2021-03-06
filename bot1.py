#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#importing the socket and string and random python librarys
import socket,string, random # will need the random for the respose prt  

#server details
SERVER = "::1"
PORT = 6667
CHANNEL = "#test" #default channel test 

IRCSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

  #set up the array of random words to send
arrayWords = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis semper leo non felis aliquam viverra."
            "Curabitur feugiat, lorem porttitor lacinia feugiat, quam velit finibus enim, convallis finibus turpis velit vel augue. Etiam sed sem in metus semper suscipit. Sed finibus orci id dolor ullamcorper, eu condimentum metus viverra. Phasellus fermentum sem quis sapien suscipit hendrerit. Praesent in diam at diam ullamcorper tincidunt eu non metus."
            "pellentesque tristique mi id feugiat. Proin in tempus enim. Proin id porta tellus"
            "Proin mollis volutpat tincidunt. Nullam euismod mi eu nulla placerat, sit amet aliquet dolor porttitor"
        ]
       
def connect():
    try:
        IRCSocket.connect((SERVER, PORT))
    except:
        print("unable to connect")
        quit()
    else:
        print("connected")
# send the server the bots usernames and nickname 
def login():
    IRCSocket.send("USER Bot networkbot server :Bot".encode('utf-8'))

    resp = IRCSocket.recv(1024).decode('utf-8')

    IRCSocket.send("NICK Bot".encode('utf-8'))
    
    resp = IRCSocket.recv(1024).decode('utf-8')
    
# join channel test
def join():
    IRCSocket.send("JOIN #test\r\n".encode('utf-8'))
    print ("joined #test channel")

#Respond to ping
def ping():
    IRCSocket.send("PONG :pingisn\r\n".encode('utf-8'))
    print("PONGED")

def listen():
    #check to see if the server is pinging 
    while (True):
        buffer = IRCSocket.recv(1024)
        message = buffer.decode()

        print(message)

        if("PING :" in message):
            ping()

        #else run the respond function sending in the message
        else:
            respond(message)
        print("responding to the message")
      
def respond(message):

    #define the start of the usename inside the command
    start = ':'

    #define the end of the usernames indide of the command msg
    end = '!'
    #number of usernames in the server
    #len(usernames) = sizeOfArray
    sizeOfArray = 4


    #find who sends the message and put it into variable usernames 
    

    usernames = message[message.find(start)+len(start):message.find(end)]

    #hello cammand 
    if ("!hello" in message and "PRVITMSG Bot" not in message):
                IRCSocket.send(("PRVITMSG #test : hello - "+ usernames+" \r\n").encode())
                print("hello")
    #slap command 
    elif ("!slap" in message and "PRVITMSG Bot" not in message):
         if ("!slap"&"" in message and "PRVITMSG Bot" not in message):
              IRCSocket.send(("PRVITMSG #test : get slapped - " + usernames +"\r\n").encode())
         else :
             IRCSocket.send(("PRVITMSG #test : get slapped - " + usernames[random.randint(sizeOfArray)] + "\r\n").encode())

    elif ("PRVITMSG Bot" in message or ("PRVITMSG Bot" in message and "!" in message)):
        
        #send the message 
         IRCSocket.send(("PRVITMSG "+ usernames +arrayWords[random.randint(0,4)] + "\r\n").encode())

#execute the run of the bot


connect()
login()
join()
listen()
