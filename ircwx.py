#----------------------------------------------------------------------
#
#   Author: Todd Lunter
#   E-mail: tlunter@gmail.com
#   Twitter: tLuntercom
#   Date Updated: 06/23/2011 T14:35
#
#----------------------------------------------------------------------

import wx
import pickle
import defaults
from serverlist import ServerListFrame
from addserver import AddServerFrame
from chat import ChatFrame
from ircclient import IRCClient

class wxIRC(wx.App):
    def OnInit(self):
        self.ServerListFrame = None
        self.AddServerFrame = None
        self.ChatFrame = None
        self.IRCClient = None
        
        try:
            pklfile = open('data.pkl','rb')
            data = pickle.load(pklfile)
            if data != None:
                self.servers = data[0]
            pklfile.close()
        except IOError:
            self.servers = defaults.servers
        except EOFError:
            self.servers = []
        
        self.SetUpServerList()
        
        return True
        
    #----------------------------------------------------------------------
    #
    #   Server Listing Section
    #
    #----------------------------------------------------------------------
    
    def SetUpServerList(self, event=None):
        if not self.ServerListFrame:
            self.ServerListFrame = ServerListFrame(None, self.servers)
        
        self.SetUpMenuBarFor(self.ServerListFrame)
        self.ServerListFrame.AddServer.Bind(wx.EVT_BUTTON, self.SetUpAddServer)
        self.ServerListFrame.Connect.Bind(wx.EVT_BUTTON, self.ConnectToServer)
        
        self.SwitchWindows(self.ServerListFrame)
                
    #----------------------------------------------------------------------
    #
    #   Add Server Section
    #
    #----------------------------------------------------------------------
    
    def SetUpAddServer(self, event=None):
        if not self.AddServerFrame:
            self.AddServerFrame = AddServerFrame(None)
            
        self.SetUpMenuBarFor(self.AddServerFrame)
        
        self.AddServerFrame.AddServer.Bind(wx.EVT_BUTTON, self.AddServer)
        
        self.SwitchWindows(self.AddServerFrame)
        
    def AddServer(self, event):
        if self.AddServerFrame.ServerPort == '':
            self.AddServerFrame.ServerPort = 6667
            
        if str(self.AddServerFrame.ServerName.GetValue()).strip() == '' or str(self.AddServerFrame.ServerURL.GetValue()).strip() == '':
            dlg = wx.MessageDialog(self.AddServerFrame, "Please add a Server URL or Name!","Missing field", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.servers.append({'name':str(self.AddServerFrame.ServerName.GetValue()).strip(),'url':str(self.AddServerFrame.ServerURL.GetValue()).strip(),'port':int(self.AddServerFrame.ServerPort.GetValue()),'username':str(self.AddServerFrame.ServerUsername.GetValue()),'password':str(self.AddServerFrame.ServerPassword.GetValue())})
            self.SetUpServerList()
    
    #----------------------------------------------------------------------
    #
    #   Chat Section
    #
    #----------------------------------------------------------------------

    def SetUpChat(self, server):
        if not self.ChatFrame:
            self.ChatFrame = ChatFrame(None)
        
        self.SetUpMenuBarFor(self.ChatFrame)
        
        self.SwitchWindows(self.ChatFrame)
                
        self.IRCClient = IRCClient(server)
        i = 0
        self.IRCClient.irc.recv(4096)
        self.IRCClient.irc.send('NICK wxirc\r\n')
        self.IRCClient.irc.send('USER wxirc wxirc wxirc :Python is awesomesauce\r\n' )
        self.IRCClient.irc.send('PRIVMSG NickServ :identify \r\n')
        self.IRCClient.irc.send('JOIN #wxirc\r\n')
        while True and i < 10:
            i += 1
            data = self.IRCClient.StartRecv()
            datasplit = data.split('\r\n')[:-1]
            print 'data: ' + str(data)
            for item in datasplit:
                itemdata = item.split(':',2)
                if len(itemdata) > 2 and len(itemdata) < 4:
                    if(itemdata[1].find('!') > -1):
                        username = itemdata[1].split('!')
                    else:
                        username = itemdata[1].split(' ')
                    self.ChatFrame.InsertRow({'username':username[0],'message':itemdata[2]})
        
    #----------------------------------------------------------------------
    #
    #   Connecting Methods
    #
    #----------------------------------------------------------------------
    
    def ConnectToServer(self, event):
        if self.ServerListFrame.ServerList.GetSelections():
            selectedServer = self.servers[self.ServerListFrame.ServerList.GetSelections()[0]]
            self.SetUpChat(selectedServer)
    
    #----------------------------------------------------------------------
    #
    #   Extra Methods
    #
    #----------------------------------------------------------------------
    
    def SetUpMenuBarFor(self, frame):
        frame.MenuBar = wx.MenuBar()
        
        frame.FileMenu = wx.Menu()
        frame.AddServerItem = wx.MenuItem(frame.FileMenu, wx.ID_ANY, u"New Server"+ u"\t" + u"CTRL+N")
        frame.FileMenu.AppendItem(frame.AddServerItem)
        frame.ServerListItem = wx.MenuItem(frame.FileMenu, wx.ID_ANY, u"Server List"+ u"\t" + u"CTRL+L")
        frame.FileMenu.AppendItem(frame.ServerListItem)
        frame.QuitItem = wx.MenuItem(frame.FileMenu, wx.ID_EXIT, u"&Quit")
        frame.FileMenu.AppendItem(frame.QuitItem)
        frame.MenuBar.Append(frame.FileMenu, u"&File") 

        frame.HelpMenu = wx.Menu()
        frame.About = wx.MenuItem(frame.HelpMenu, wx.ID_ABOUT, u"&About")
        frame.HelpMenu.AppendItem(frame.About)
        frame.MenuBar.Append(frame.HelpMenu, u"&Help") 

        frame.SetMenuBar(frame.MenuBar)
        
        self.Bind(wx.EVT_MENU, self.SetUpAddServer, frame.AddServerItem)
        self.Bind(wx.EVT_MENU, self.SetUpServerList, frame.ServerListItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, frame.QuitItem)
    
    def OnQuit(self, event=None):
        pklfile = open('data.pkl','wb')

        data = [self.servers]
        pickle.dump(data, pklfile)

        pklfile.close()
        
        self.SwitchWindows(None)
        
    def SwitchWindows(self, currentFrame = None):
        if currentFrame == None:
            if self.ChatFrame:
                self.ChatFrame.Close(True)
                self.ChatFrame = None

            if self.AddServerFrame:
                self.AddServerFrame.Close(True)
                self.AddServerFrame = None

            if self.ServerListFrame:
                self.ServerListFrame.Close(True)
                self.ServerListFrame = None
        else:
            if self.ServerListFrame != currentFrame and self.ServerListFrame:
                self.ServerListFrame.Close(True)
                self.ServerListFrame = None

            if self.AddServerFrame != currentFrame and self.AddServerFrame:
                self.AddServerFrame.Close(True)
                self.AddServerFrame = None

            if self.ChatFrame != currentFrame and self.ChatFrame:
                self.ChatFrame.Close(True)
                self.ChatFrame = None
                
            currentFrame.Show()

if __name__ == '__main__':
    irc = wxIRC(0)
    irc.MainLoop()
    
