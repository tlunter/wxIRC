import wx

class ChatPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        
        #Full panel sizer
        PageSizer = wx.BoxSizer(wx.VERTICAL)
        
        #Chat List
        self.ChatList = wx.ListCtrl(self, wx.ID_ANY, wx.Point(-1,-1), wx.Size(-1,-1), wx.LC_NO_SORT_HEADER|wx.LC_REPORT|wx.LC_VRULES)
        
        PageSizer.Add(self.ChatList, 1, wx.BOTTOM|wx.EXPAND, 5)
        
        #Send text form sizer
        SendFormSizer = wx.BoxSizer(wx.HORIZONTAL)

        #Send text form textbox
        self.SendFormText = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(-1,-1), wx.Size(-1,-1), 0)
        SendFormSizer.Add(self.SendFormText, 1, wx.ALIGN_RIGHT|wx.ALIGN_TOP|wx.LEFT|wx.RIGHT, 5)

        #Send text form submit
        self.Send = wx.Button(self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        SendFormSizer.Add(self.Send, 0, wx.RIGHT, 5)

        PageSizer.Add(SendFormSizer, 0, wx.EXPAND, 5)
        
        self.SetSizer(PageSizer)
        self.Layout()
        PageSizer.Fit(self)
        
        self.ChatList.InsertColumn(0, 'Username', wx.LIST_FORMAT_LEFT, 100)
        self.ChatList.InsertColumn(1, 'Message', wx.LIST_FORMAT_LEFT, (self.ConvertDialogSizeToPixels(self.GetSize()).GetWidth())-100)