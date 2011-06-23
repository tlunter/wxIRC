#----------------------------------------------------------------------
#
#   Author: Todd Lunter
#   E-mail: tlunter@gmail.com
#   Twitter: tLuntercom
#   Date Updated: 06/23/2011 T14:35
#
#----------------------------------------------------------------------

import wx

class AddServerFrame(wx.Frame):
    def __init__(self, parent):
		wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = u"Server Information", pos = wx.DefaultPosition, size = wx.Size(270,240), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		
		self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
		
		fgSizer1 = wx.FlexGridSizer(6, 2, 10, 30)
		fgSizer1.SetFlexibleDirection(wx.BOTH)
		fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
		
		self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"Server Name:", wx.DefaultPosition, wx.DefaultSize, 0)
		fgSizer1.Add(self.m_staticText1, 1, wx.TOP|wx.LEFT, 20)
		
		self.ServerName = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		fgSizer1.Add(self.ServerName, 1, wx.TOP|wx.LEFT, 20)
		
		self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"Server URL:", wx.DefaultPosition, wx.DefaultSize, 0)
		fgSizer1.Add(self.m_staticText1, 1, wx.LEFT, 20)
		
		self.ServerURL = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		fgSizer1.Add(self.ServerURL, 1, wx.LEFT, 20)
		
		self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"Server Port:", wx.DefaultPosition, wx.DefaultSize, 0)
		fgSizer1.Add(self.m_staticText3, 1, wx.LEFT, 20)
		
		self.ServerPort = wx.TextCtrl(self, wx.ID_ANY, u"6667", wx.DefaultPosition, wx.Size(50,-1), 0)
		self.ServerPort.SetMaxLength(5) 
		fgSizer1.Add(self.ServerPort, 1, wx.LEFT, 20)
		
		self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"Username:", wx.DefaultPosition, wx.DefaultSize, 0)
		fgSizer1.Add(self.m_staticText2, 1, wx.LEFT, 20)
		
		self.ServerUsername = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		fgSizer1.Add(self.ServerUsername, 1, wx.LEFT, 20)
		
		self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Password:", wx.DefaultPosition, wx.DefaultSize, 0)
		fgSizer1.Add(self.m_staticText4, 1, wx.LEFT, 20)
		
		self.ServerPassword = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD)
		fgSizer1.Add(self.ServerPassword, 1, wx.LEFT, 20)
		
		fgSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)
		
		self.AddServer = wx.Button(self, wx.ID_ANY, u"Add Server", wx.DefaultPosition, wx.DefaultSize, 0)
		fgSizer1.Add(self.AddServer, 0, wx.LEFT, 20)
		
		self.SetSizer(fgSizer1)
		self.Layout()
		
		self.Center(wx.BOTH)