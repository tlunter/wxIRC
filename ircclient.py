#----------------------------------------------------------------------
#
#   Author: Todd Lunter
#   E-mail: tlunter@gmail.com
#   Twitter: tLuntercom
#   Date Updated: 06/23/2011 T17:33
#
#----------------------------------------------------------------------

import socket
import re

class IRCClient():
    def __init__(self, server, chat_frame):
        self._chat_frame = chat_frame
        self._irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server = server
        self._incomplete_data = ''
        self._running = False
        self._count = {}
        self._regex = r':((?P<USERNAME>[^!]+)!)?(?P<HOST>\S+)\s+(?P<ACTION>\S+)\s+:?(?P<CHANNEL>\S+)\s*(?:(?::|[+-]+)(?P<MESSAGE>.*))?'
        
    def StartRecv(self):
        self._irc.connect((str(self._server['url']) , self._server['port']))
        self.StartSend('NICK ' + self._server['username'] + '\r\n')
        self.StartSend('USER ' + self._server['username'] + ' ' + self._server['username'] + '_ ' + self._server['username'] + '__ :wxIRC\r\n' )
        
        while True:
            if not self._running:
                
                self.SetRunning(True)
                
                new_data = self._irc.recv(4096)
                data = str(self._incomplete_data) + str(new_data)
                datasplit = data.split('\r\n')                
                self._incomplete_data = datasplit.pop()
                
                for item in datasplit:
                
                    if(item.find('PING') != -1):
                        ping = 'PONG ' + item.split()[1] + '\r\n'
                        self.StartSend(ping)
                    
                    matches = re.match(self._regex, item)
                    
                    if matches:
                        
                        print matches.groupdict()
                        
                        if matches.group('MESSAGE') and matches.group('ACTION') != 'MODE':
                            
                            real_data = {'username':matches.group('USERNAME') if matches.group('USERNAME') != None else '', 'message':matches.group('MESSAGE')}
                            channel = matches.group('CHANNEL') if matches.group('CHANNEL') != '*' else self._server['username']

                            try:
                                self._count[channel]
                            except KeyError:
                                self._count[channel] = 0
                            
                            self._chat_frame.SendData(real_data, self._count[channel], channel)
                            
                            self._count[channel] += 1
                            
                            if matches.group('USERNAME') == 'NickServ' and matches.group('MESSAGE').find('registered') != -1:
                                self._irc.send('PRIVMSG NickServ :identify ' + self._server['password'] + '\r\n')
                                self._irc.send('JOIN #wxirc\r\n')
                                
                        if matches.group('ACTION') == 'JOIN' or matches.group('ACTION') == 'PART':
                            
                            username = matches.group('USERNAME')
                            
                            if matches.group('ACTION') == 'JOIN':
                                real_data = {'username':str(matches.group('CHANNEL')), 'message':str(username) + ' has just joined.'}
                            if matches.group('ACTION') == 'PART':
                                real_data = {'username':str(matches.group('CHANNEL')), 'message':str(username) + ' has quit: (Message: ' + str(matches.group('MESSAGE')) + ').'}
                                
                            channel = matches.group('CHANNEL') if matches.group('CHANNEL') != '*' else self._server['username']

                            try:
                                self._count[channel]
                            except KeyError:
                                self._count[channel] = 0
                            
                            self._chat_frame.SendData(real_data, self._count[channel], channel)
                            
                            self._count[channel] += 1
                            
                        #if matches.group('ACTION')
                                
                self.SetRunning(False)
        
    def SetRunning(self, value):
        self._running = value
        
    def StartSend(self, message):
        print message
        self._irc.send(message)
        