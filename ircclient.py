import socket

class IRCClient():
    def __init__(self, server):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((str(server['url']) , server['port']))
        
    def StartRecv(self):
        self.irc.send('JOIN #reddit')
        return self.irc.recv(4096)