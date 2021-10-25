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
                
#Class to define user object
class User:
    #initialise user attributes
    def __init__(self, socket, addr, name):
        self.socket = socket
        self.address = addr
        self.nickname = name
        
#initialise default channels
channels = [Channel("test"), Channel("channel2")] 
awaitingPrivate = []

#listen and accept clients onto the server
def connectUser(s):
    s.listen()
    while True:

        try:
            socket, addr = s.accept()
        except:
            print("test")

        print(f"{str(addr)} has connected")

        while True:
            socket.send('NICK'.encode('utf-8')) #server sends keyword to client to receive nickname
            nickname = socket.recv(1024).decode('utf-8') 
            
            for c in channels:
                for u in c.users:
                    if u.nickname == nickname:
                        sendMessage(f'sorry nickname {nickname} already taken, please try again')
                        continue
            break

        user = User(socket, addr, nickname)
     
        sendMessage(f'welcome to the server {user.nickname}!\n', user)

        thread = handleClient(user)
        thread.start()
        
#print available channels 
def listChannels():
    msg = "\nplease select a channel to join:"
    for channel in channels:
        msg = msg + "\n     - #" + channel.name
    msg = msg + '\n' 
    return msg

#print commands
def listUserCommands():
    msg = "---------User Commands------------"
    msg = msg + "\n!help - show this list"
    msg = msg + "\n!channel - name of current channel"
    msg = msg + "\n!leave - leave channel"
    msg = msg + "\n!list - list nickames on current channel"
    msg = msg + "\n!listall - list nicknames of all users on the server"
    msg = msg + "\n!count - count number of users in the current channel"
    msg = msg + "\n!private - private message a user"
    msg = msg + "\n!exit - disconnect from server\n"
    return msg

#send message to users in a channel
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

#allow users to choose channel to join        
def pickChannel(user):
    while(True):
            sendMessage(listChannels(), user)
            channelName = safePipe(user)

            valid = False
            for channel in channels:
                if channel.name in channelName:
                    channel.join(user)
                    valid = True
                    print(f'user {user.nickname} has has joined channel {channel.name}')
                    return(channel)
                
            sendMessage("\nPlease enter a valid channel name\n", user)

#allow users to send requests to chat privately
def privateRequest(user):
    sendMessage("Which user would you like to chat provately to?", user)
    msg = safePipe(user)
    recip = None
    valid = False
    for c in channels:
        for u in c.users:
            if u.nickname == msg:
                recip = u
                valid = True
    
    if valid != True:
        sendMessage("Please enter a valid user name \n", user)
        return

    pair = [user, recip]

    if pair not in awaitingPrivate:
        awaitingPrivate.append(pair)

    sendMessage(f'user {user.nickname} has requested to speak privately, do you accept? [!accept {user.nickname}/!decline {user.nickname}]',recip)
    sendMessage(f'awaiting user {recip.nickname} to join private chat, type !stop to exit', user)

    while True:
        msg = safePipe(user)
        
        if msg == "!stop" and pair in awaitingPrivate:
            sendMessage(f'user {user.nickname} no longer requests a private chat', recip)
            awaitingPrivate.remove(pair)
            return
        elif msg == "!stop":
            sendMessage(f'user {user.nickname} has left the private chat, type !stop to exit', recip)
            return
        elif pair not in awaitingPrivate:
            sendMessage(f'|Private| {user.nickname}: {msg}', recip)
        else:
            sendMessage(f'user {recip.nickname} not yet accepted private chat. Type !stop to exit')
        
#allows user to accept request
def privateAccept(user, msg):
    recip = None
    recipNickname = msg[8:]
    for c in channels:
        for u in c.users:
            if u.nickname == recipNickname:
                recip = u
    
    pair = [recip, user]
    if pair not in awaitingPrivate:
        sendMessage("Incorrect username entered please try again", user)
        return

    awaitingPrivate.remove(pair)

    sendMessage(f'you have now joined a private chat with {recip.nickname}, type !stop to exit', user)
    sendMessage(f'user {user.nickname} has joined the private chat', recip)

    while True:
        msg = safePipe(user)

        if msg == "!stop":
            sendMessage(f'user {user.nickname} has left the private chat, type !stop to exit', recip)
            return
        else:
            sendMessage(f'|Private| {user.nickname}: {msg}', recip)

#allows users to decline request
def privateDecline(user, msg):
    recip = None
    recipNickname = msg[8:]
    for c in channels:
        for u in c.users:
            if u.nickname == recipNickname:
                recip = u
    
    pair = [recip, user]
    if pair not in awaitingPrivate:
        sendMessage("Incorrect username entered please try again", user)
        return

    sendMessage(f'user {user.nickname} has declined to private chat', recip)
    awaitingPrivate.remove(pair)

#class to define client object
class handleClient(threading.Thread):
    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user
    
    def run(self):
        global channels 
        global awaitingPrivate

        self.channel = pickChannel(self.user)

        sendMessage(listUserCommands(), self.user)

        while True:
            msg = safePipe(self.user)

            if msg == "!help":
                sendMessage(listUserCommands(), self.user)
            elif msg == "!channel":
                sendMessage(f'\n{self.channel.name}', self.user)
            elif msg == "!leave":
                self.channel.leave(self.user)
                self.channel = pickChannel(self.user)
            elif msg == "!list":
                for u in self.channel.users:
                    sendMessage(f'{u.nickname}\n', self.user)
            elif msg == "!listall":
                for c in channels:
                    for u in c.users:
                        sendMessage(f'{u.nickname}\n', self.user)
            elif msg == "!count":
                i = 0
                for c in channels:
                    for u in c.users:
                        i += 1
                sendMessage(str(i), self.user)
            elif msg == "!private":
                privateRequest(self.user)
            elif "!accept" in msg:
                privateAccept(self.user, msg)
            elif "!decline" in msg:
                privateDecline(self.user, msg)
            elif msg == "!exit":
                self.channel.leave(self.user)
                sendMessage("EXIT", self.user)
                self.user.socket.shutdown
                print(f'user {self.user.nickname} has disconnected')
                break
            else:
                self.channel.messageChannel(self.user, msg)


connectUser(s)
