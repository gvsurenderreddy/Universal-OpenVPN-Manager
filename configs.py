"""
<Universal OpenVPN Manager - A GUI front-end for OpenVPN>
Copyright (C) 2016, Simon Wu, <swprojects@gmx.com>
 
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Softwares
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import wx
from os import walk
from base import BasePanel

CONFIGPATH = "c:/Program Files/OpenVPN/config/"

class ConfigsList(wx.ListCtrl):

    def __init__(self, parent):
        wx.ListCtrl.__init__(
                            self, 
                            parent,
                            style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        
        columns = ["Config",
                   "Path",
                   "Favorite",
                   "Key",
                   "File"]
                   
        for col in columns:         
            self.AppendColumn(col)
        
        self.RefreshConfigs()
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
        
    def RefreshConfigs(self, msg=None):
        """ search for ovpn configs and populate list """
        self.DeleteAllItems()
        configs = [] 
        for root, dirs, files in walk(CONFIGPATH):
            for f in files:
                if f[-5:] == ".ovpn":
                    configs.append([f, root])
        print(configs)   
        
        for c, root in configs:
            label = c[:-5]
            starred = False
            self.Append([label, root, str(starred)])
    
    def OnListItemActivated(self, event):
        """ send config name and path to DoConnect for connection """
        index = event.Index
        config = self.GetItem(index, 0).GetText()
        path = self.GetItem(index, 1).GetText()
        msg = [config, path]        
        pub.sendMessage("DoConnect", msg)
        
class Configs(BasePanel):
    """ navigate different """
    
    def __init__(self, parent):
        BasePanel.__init__(self, 
                           parent)
                            
        sizer = wx.BoxSizer(wx.VERTICAL)
        list = ConfigsList(self)
        sizer.Add(list, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)
        # self.GetParent().Fit()
        # self.Refresh()
        # self.Layout()
        