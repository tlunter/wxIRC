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

class ServerListFrame(wx.Frame):
    def __init__(self, parent, servers):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = u"Server List", pos = wx.DefaultPosition, size = wx.Size(200,350), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.SetSizeHintsSz(wx.DefaultSize, wx.Size(200,300))

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        fgSizer3 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.ServerList = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200,300), [], wx.LB_SINGLE|wx.SUNKEN_BORDER)
        self.SetServers(servers)

        fgSizer3.Add(self.ServerList, 0, wx.EXPAND, 5)

        gSizer2 = wx.GridSizer(1, 2, 0, 0)

        self.AddServer = wx.Button(self, wx.ID_ANY, u"New Server", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.AddServer, 0, wx.EXPAND|wx.RIGHT, 5)

        self.Connect = wx.Button(self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.Connect, 0, wx.ALIGN_RIGHT|wx.EXPAND|wx.RIGHT, 5)

        fgSizer3.Add(gSizer2, 0, 0, 5)

        bSizer3.Add(fgSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Center(wx.BOTH)
        
    def SetServers(self,servers):
        self.ServerListChoices = servers
        self.ServerList.Set([server['name'] for server in self.ServerListChoices])
        
    def OnQuit(self, event):
        pklfile = open('data.pkl','wb')
        
        data = [self.ServerListChoices]
        pickle.dump(data, pklfile)

        pklfile.close()
        
        self.Destroy()