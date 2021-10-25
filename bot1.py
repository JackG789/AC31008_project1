#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#importing the socket and string and random and argparse python librarys
import socket,string, random,argparse # will need the random for the respose prt  

#server details
SERVER = "10.0.42.17"
PORT = 6667
CHANNEL = "#test" #default channel test 
BOTNICK = "Bot"

IRCSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  #set up the array of random words to send
arrayWords = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis semper leo non felis aliquam viverra."
            "Curabitur feugiat, lorem porttitor lacinia feugiat, quam velit finibus enim, convallis finibus turpis velit vel augue. Etiam sed sem in metus semper suscipit. Sed finibus orci id dolor ullamcorper, eu condimentum metus viverra. Phasellus fermentum sem quis sapien suscipit hendrerit. Praesent in diam at diam ullamcorper tincidunt eu non metus."
            "pellentesque tristique mi id feugiat. Proin in tempus enim. Proin id porta tellus"
            "Proin mollis volutpat tincidunt. Nullam euismod mi eu nulla placerat, sit amet aliquet dolor porttitor"
        ]
       
#parsing commands
parser =argparse.ArgumentParser(description='bot command parameters')
parser.add_argument("--hostname",type=str ,help="enter the server you wish the bot to connect to",required=False)
parser.add_argument("--port",type=int,help="enter the port you wish the bot to connect though",required=False)
parser.add_argument("--name",type=str ,help="enter what you wish the bot to be called",required=False)
parser.add_argument("--channel",type=str ,help="enter the channel you wish the bot to join ",required=False)

args = parser.parse_args()
if args.hostname:
    SERVER = args.hostname
if args.port:
    PORT = str(args.port)
if args.name:
    BOTNICK = args.name
if args.channel:
    CHANNEL = args.channel

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
    IRCSocket.send(("USER " + BOTNICK+ " networkbot  server :Bot\r\n").encode())
    IRCSocket.send(("NICK " + BOTNICK + " \r\n").encode())
    print ("logged in as Bot")
    
# join channel test
def join():
    IRCSocket.send(("JOIN "+ CHANNEL + "\r\n").encode())
    print ("joined "+CHANNEL+ "channel")

#Respond to ping
def ping():
    IRCSocket.send("PONG :pingisn\r\n".encode())
    print("PONGED")

def listen():
    #check to see if the server is pinging 
    while (True):
        buffer = IRCSocket.recv(1024)
        message = buffer.decode()

        
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
    
    


    #find who sends the message and put it into variable usernames 
    

    usernames = message[message.find(start)+len(start):message.find(end)]
    
    #count the people in the channel
    #IRCSocket.send(("!count\r\n").encode)
    #if (int in message and "PRVITMSG Bot" not in message):
       # sizeOfArray = message  

    sizeOfArray=4 #couldnet get the count working for how many people in the channel so sets to 4

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
