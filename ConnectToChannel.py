import socket
import sys


user = []
channel = []

def connectToChannel (userName, channelName):
    if userName in user and channelName in channel:

        if userName in channel[channelName] and channelName in user[username]:
            print("user already in channel")

        else:

            user[userName].append(channelName)
            channel[channelName].append(userName)
            print("user connected")
