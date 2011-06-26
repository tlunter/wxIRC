#----------------------------------------------------------------------
#
#   Author: Todd Lunter
#   E-mail: tlunter@gmail.com
#   Twitter: tLuntercom
#   Date Updated: 06/23/2011 T14:35
#
#----------------------------------------------------------------------

import wx
from chatpage import ChatPage

class ChatFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        
        self.SetSizeHintsSz(wx.Size(450, 225), wx.DefaultSize)
        
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.ChannelTabs = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1,-1), 0)
        
        self.Channels = {}
        
        FrameSizer.Add(self.ChannelTabs, 1, wx.EXPAND|wx.ALL, 5)
        
        self.SetSizer(FrameSizer)
        self.Layout()
        FrameSizer.Fit(self)
        
        self.Center(wx.BOTH)
		
    def InsertRow(self, data, count, channel):
        try:
            self.Channels[channel]
        except KeyError:
            self.Channels[channel] = ChatPage(self.ChannelTabs)
            self.ChannelTabs.AddPage(self.Channels[channel], channel, True)
            
        CurrentChannel = self.Channels[channel].ChatList
        
        count = CurrentChannel.GetItemCount() if count != CurrentChannel.GetItemCount() else count
        
        CurrentChannel.InsertStringItem(count,' ' + str(data['username']))
        CurrentChannel.SetStringItem(count,1,' ' + str(data['message']))
        CurrentChannel.ScrollList(0, count)
        
    def SendData(self, data, count, channel):
        wx.CallAfter(self.InsertRow, {'username':data['username'],'message':data['message']}, count, channel)