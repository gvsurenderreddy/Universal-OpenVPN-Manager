import wx
from base import *
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

LOCATIONS = ["USA","France","Germany","United Kingdom","Ukraine","Hong Kong"]

class SidebarList(wx.ListCtrl):
    """ navigate different """
    
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, 
                             parent,
                             style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_NO_HEADER|wx.LC_HRULES)
                            
        self.AppendColumn("Sidebar")        
                
        self.SetFont(SIDEBARFONT)               
        strmax = []
        items = ["-----MAIN-----",
                 "All Configs",
                 "Recently Used",
                 "Starred",
                 "Command Flags",
                 "Preferences",
                 "-----Protocol-----",
                 "TCP",
                 "UDP",
                 "-----Locations-----"]
                 
        for item in items:
            strmax.append(len(item))
            self.InsertItem(self.GetItemCount(), item)
            
        for loc in LOCATIONS:
            strmax.append(len(loc))
            if loc == "separator":
                self.InsertItem(self.GetItemCount(), "-"*10)
                continue
            self.InsertItem(self.GetItemCount(), loc)
            
        dc = wx.ScreenDC()
        dc.SetFont(SIDEBARFONT)

        text = "*"*max(strmax)
        maxtextwidth, _ = dc.GetTextExtent(text)
        # (width, height) in pixels
        # print  dc.GetTextExtent(text))
        
        self.SetSize(250, -1)
        self.SetColumnWidth(0, maxtextwidth)
        
        #Bindings
        self.Bind(wx.EVT_MOTION, self.OnSidebarMotion)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSidebarListItemSelected)
        
    def OnSidebarMotion(self, event): 
        pos = event.GetPosition()
        row, _ = self.HitTest(pos) 
        
        if row == -1:
            return
            
        item_txt = self.GetItem(row, 0).GetText()   
        if "-" in item_txt:
            return
        self.Select(row)
        
    def OnSidebarListItemSelected(self, event=None): 
        item = event.Index
        if item == -1:
            return
            
        item_txt = self.GetItem(item).GetText()   
        pub.sendMessage("PubSubChangeMainPanel", item_txt)
        
        
        
class Sidebar(BasePanel):
    """ navigate different """
    
    def __init__(self, parent):
        BasePanel.__init__(self, parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        list = SidebarList(self)
        sizer.Add(list, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)
        