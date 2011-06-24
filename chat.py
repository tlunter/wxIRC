#----------------------------------------------------------------------
#
#   Author: Todd Lunter
#   E-mail: tlunter@gmail.com
#   Twitter: tLuntercom
#   Date Updated: 06/23/2011 T14:35
#
#----------------------------------------------------------------------

import wx

class ChatFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size(500,300), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.ServerList = wx.ListCtrl(self, wx.ID_ANY, wx.Point(-1,-1), wx.Size(450,225), wx.LC_NO_SORT_HEADER|wx.LC_REPORT|wx.LC_VRULES)
        bSizer4.Add(self.ServerList, 1, wx.BOTTOM|wx.EXPAND, 5) 
        self.ServerList.InsertColumn(0, 'Username', wx.LIST_FORMAT_LEFT, 100)
        self.ServerList.InsertColumn(1, 'Message', wx.LIST_FORMAT_LEFT, (500-100))

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer5.SetMinSize(wx.Size(-1,45)) 
        self.TextBox = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(-1,-1), wx.Size(-1,-1), 0)
        bSizer5.Add(self.TextBox, 1, wx.ALIGN_RIGHT|wx.ALIGN_TOP|wx.TOP|wx.LEFT|wx.RIGHT, 3)

        self.Send = wx.Button(self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        bSizer5.Add(self.Send, 0, wx.ALIGN_TOP|wx.RIGHT, 5)

        bSizer4.Add(bSizer5, 0, wx.EXPAND|wx.FIXED_MINSIZE, 5)

        self.SetSizer(bSizer4)
        self.Layout()
        self.StatusBar = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)

        self.Center(wx.BOTH)
		
    def InsertRow(self, data):
        ItemCount = self.ServerList.GetItemCount()
        self.ServerList.InsertStringItem(ItemCount,' ' + str(data['username']))
        self.ServerList.SetStringItem(ItemCount,1,' ' + str(data['message']))
        
    def SendData(self, data):
        datasplit = data.split('\r\n')[:-1]
        for item in datasplit:
            itemdata = item.split(':',2)
            if len(itemdata) > 2 and len(itemdata) < 4:
                if(itemdata[1].find('!') > -1):
                    username = itemdata[1].split('!')
                else:
                    username = itemdata[1].split(' ')
                self.InsertRow({'username':username[0],'message':itemdata[2]})
                self.ServerList.ScrollList(0,self.ServerList.GetItemCount())