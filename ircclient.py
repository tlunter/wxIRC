#----------------------------------------------------------------------
#
#   Author: Todd Lunter
#   E-mail: tlunter@gmail.com
#   Twitter: tLuntercom
#   Date Updated: 06/23/2011 T17:33
#
#----------------------------------------------------------------------

import socket

class IRCClient():
    def __init__(self, server):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((str(server['url']) , server['port']))
        
    def StartRecv(self):
        return self.irc.recv(4096)