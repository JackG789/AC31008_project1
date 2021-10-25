import socket
import threading

HOST = "::1"
PORT = 6667
#socket initialistion
s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)

try:
    s.bind((HOST,PORT))
except:
    print("address currently in use")
    exit()

print(f'listening on port {str(PORT)}....')

#Class to define channel object
class Channel:
    #initialise object attributes
    def __init__(self, name):
        self.name = name
        self.users = []

    #add user to the list of users within the channel and message all users letting them know they have joined
    def join(self, user):
        self.users.append(user)
        for u in self.users:
            sendMessage(f'user {user.nickname} has joined the chat', u)

    #remove user from list of users and message all users letting them know they have left
    def leave(self, user):
        self.users.remove(user)
        for u in self.users:
            sendMessage(f'user {user.nickname} has left the channel', u)

#message all users in the channel
    def messageChannel(self, user, message):
        if message == "":
            return
        m = f"{user.nickname}: {message}"
        for u in self.users:
            if u != user:
                sendMessage(m, u) 
    
    def privateMessageChannel(self, user, message):
        if message == "":
            return
        m = f"|private| {user.nickname}: {message}"

class User:
    def __init__(self, socket, addr, username, nickname, realname):
        self.socket = socket
        self.address = addr
        self.username = username
        self.nickname = nickname
        self.realname = realname

channels = [Channel("test"), Channel("channel2")] 

def connectUser(s):
    s.listen()
    while True:

        try:
            socket, addr = s.accept()
        except:
            print(f'{str(addr)} error connecting')

        print(f"{str(addr)} has connected")

        username = ""
        nickname = ""
        realname = ""

        while True:
            
            msg = socket.recv(1024).decode('utf-8') 

            if "USER" not in msg:
                socket.send("please enter a correct USER command".encode('utf-8'))
                continue

            for c in channels:
                for u in c.users:
                    if u.username == username:
                        socket.send(f'sorry username {usename} already taken, please try again'.encode('utf-8'))
                        continue
            
            cmd = msg.split()

            username = cmd[1]
            realname = cmd[4]

            socket.send("Username Valid".encode('utf-8'))

            break
        
        while True:
            msg = socket.recv(1024).decode('utf-8') 

            if "NICK" not in msg:
                socket.send("please enter a correct NICK command".encode('utf-8'))
                continue
            
            cmd = msg.split()
            nickname = cmd[1]

            break


        user = User(socket, addr, username, nickname, realname)
     
        sendMessage(f'welcome to the server {user.nickname}!\n', user)

        thread = handleClient(user)
        thread.start()

def listChannels():
    for channel in channels:
        msg = msg + "\n     - #" + channel.name
    msg = msg + '\n' 
    return msg

def listUserCommands():
    msg = "---------User Commands------------"
    msg = msg + "\nHELP - show this list"
    msg = msg + "\nCHANNELS - list all channels"
    msg = msg + "\nJOIN - join a channel"
    msg = msg + "\nPING - PING server and recieve PONG"
    msg = msg + "\nLIST - list nickames on current channel"
    msg = msg + "\nLISTALL - list nicknames of all users on the server"
    msg = msg + "\nCOUNT - count number of users in the current channel"
    msg = msg + "\nPRVITMSG - private message a user"
    msg = msg + "\nEXIT - disconnect from server\n"
    return msg

def sendMessage(msg, user):
    try:
        user.socket.send(msg.encode('utf-8'))
    except:
        user.socket.close()
        print(f'user {user.nickname} disconnected unexpectedly')
        for c in channels:
            for u in c.users:
                if u == user:
                    c.leave(user)
        exit()


def safePipe(user):
    try:
        return user.socket.recv(1024).decode('utf-8')
    except:
        user.socket.close()
        print(f'user {user.nickname} disconnected unexpectedly')
        for c in channels:
            for u in c.users:
                if u == user:
                    c.leave(user)
        exit()

def join(user, msg):
    chanName = msg.strip().split()[1][1:]

    print(chanName)

    channel = None

    for c in channels:
        if c.name == chanName:
            channel = c

    if channel == None:
            sendMessage("\nPlease enter a valid channel name", user)
            return

    for c in channels:
        for u in c.users:
            if u == user:
                c.leave(user)

    channel.join(user)
    print(f'user {user.nickname} has has joined channel {channel.name}')

def private(user, msg):
    cmd = msg.split(":")
    message = cmd[1]

    recipients = cmd[1].split().pop()
    for recipient in recipients:
        if recipient[0] == '#':
            for channel in channels:
                if channel.name == recipient[1:]:
                    channel.privateMessageChannel(user, message)
        else:
            for channel in channels:
                for u in channel.users:
                    if u.nickname == recipient:
                        sendMessage(f"|Private| {user.nickname}: {message}", u)



class handleClient(threading.Thread):
    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user

    def run(self):
        global channels 
        global awaitingPrivate

        self.channel = None

        sendMessage(listUserCommands(), self.user)

        while True:
            msg = safePipe(self.user)
            
            print(msg)

            if msg == "HELP":
                sendMessage(listUserCommands(), self.user)
            elif msg == "CHANNELS":
                sendMessage(listChannels(), self.user)
            elif "JOIN" in msg:
                join(self.user, msg)
            elif msg == "PING":
                sendMessage("PONG", user)
            elif msg == "LIST":
                for u in self.channel.users:
                    sendMessage(f'{u.nickname}\n', self.user)
            elif msg == "LISTALL":
                for c in channels:
                    for u in c.users:
                        sendMessage(f'{u.nickname}\n', self.user)
            elif msg == "COUNT":
                i = 0
                for c in channels:
                    for u in c.users:
                        i += 1
                sendMessage(str(i), self.user)
            elif "PRVITMSG" in msg:
                private(self.user, msg)
            elif msg == "EXIT":
                self.channel.leave(self.user)
                sendMessage("EXIT", self.user)
                self.user.socket.shutdown
                print(f'user {self.user.nickname} has disconnected')
                break
            else:
                self.channel.messageChannel(self.user, msg)


connectUser(s)