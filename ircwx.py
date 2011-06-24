#----------------------------------------------------------------------
#
#   Author: Todd Lunter
#   E-mail: tlunter@gmail.com
#   Twitter: tLuntercom
#   Date Updated: 06/23/2011 T17:33
#
#----------------------------------------------------------------------

import wx
import pickle
import defaults
from serverlist import ServerListFrame
from addserver import AddServerFrame
from chat import ChatFrame
from ircclient import IRCClient
from threading import *
import thread
import time

EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)
    
class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
        
class WorkerThread(Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window, ircclient):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._ircclient = ircclient
        self._notify_window = notify_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        """Run Worker Thread."""
        if self._want_abort:
            wx.PostEvent(self._notify_window, ResultEvent(-1))
            return
        
        data = self._ircclient.StartRecv()
        
        print "Data: " + data
        wx.PostEvent(self._notify_window, ResultEvent(data))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1

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
        
        EVT_RESULT(self.ChatFrame,self.OnResult)
        
        self.worker = None
        
        self.background = thread.start_new_thread(self.ChatStart, ())
        
        self.IRCClient.irc.send('NICK wxirc\r\n')
        self.IRCClient.irc.send('USER wxirc wxirc wxirc :Python is awesomesauce\r\n' )
        self.IRCClient.irc.send('PRIVMSG NickServ :identify wxirc1\r\n')
        self.IRCClient.irc.send('JOIN #wxirc\r\n')
        
    def ChatStart(self):
        if not self.worker:
            self.worker = WorkerThread(self.ChatFrame, self.IRCClient)
        
    def OnResult(self, event):
        if event.data != -1:
            if event.data.find ( 'PING' ) != -1:
                self.IRCClient.irc.send('PONG ' + event.data.split()[1] + '\r\n')
            wx.CallAfter(self.ChatFrame.SendData, event.data)
            self.worker = None
            self.ChatStart()
        else:
            self.background.exit()
            
        
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
        if self.worker:
            self.worker.abort()
                    
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
    
