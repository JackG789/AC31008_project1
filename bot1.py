  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#importing the socket and string and random python librarys
import socket, string,  random # will need the random for the respose prt  

#server details
SERVER = "localhost"
PORT = 6667
CHANNEL = "#test" 

IRCSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    IRCSocket.connect((SERVER, PORT))
    
# send the server the bots username and nickname 
def login():
    IRCSocket.send("USER Bot networkbot server :Bot\r\n".encode())
    IRCSocket.send("NICK Bot\r\n".encode())
    
# join channel test
def join():
    IRCSocket.send("JOIN #test\r\n".encode())

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
        
      
def respond(message):

    #define the start of the usename inside the command
    start = ':'

    #define the end of the username indide of the command msg
    end = '!'
    #number of usernames in the server
    len(username) = sizeOfArray

    #find who sends the message and put it into variable username 
    

    username = message[message.find(start)+len(start):message.find(end)]

    #hello cammand 
    if ("!hello" in message and "PRVITMSG Bot" not in message):
                IRCSocket.send(("PRVITMSG #test : hello - "+ username" \r\n").encode())
                print("hello")
    #slap command 
     elif ("!slap" in message and "PRVITMSG Bot" not in message):
            if ("!slap"&"" in message and "PRVITMSG Bot" not in message):
             IRCSocket.send(("PRVITMSG #test : get slapped - " + username "\r\n").encode())
            else :
                IRCSocket.send(("PRVITMSG #test : get slapped - " + username[random.randint(sizeOfArray)] + "\r\n").encode())

     elif ("PRVITMSG Bot" in message or ("PRVITMSG Bot" in message and "!" in message)):
         
         #set up the array of random words to send
        arrayWords = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis semper leo non felis aliquam viverra."
            "Curabitur feugiat, lorem porttitor lacinia feugiat, quam velit finibus enim, convallis finibus turpis velit vel augue. Etiam sed sem in metus semper suscipit. Sed finibus orci id dolor ullamcorper, eu condimentum metus viverra. Phasellus fermentum sem quis sapien suscipit hendrerit. Praesent in diam at diam ullamcorper tincidunt eu non metus."
            "pellentesque tristique mi id feugiat. Proin in tempus enim. Proin id porta tellus"
            "Proin mollis volutpat tincidunt. Nullam euismod mi eu nulla placerat, sit amet aliquet dolor porttitor"

        ]
        
        #send the message 
         IRCSocket.send(("PRVITMSG "+ username +arrayWords[random.randint(0,4)] + "\r\n").encode())

#execute the run of the bot


connect()
login()
join()
listen()

