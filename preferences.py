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
from base import BasePanel

class PreferencesList(wx.ListCtrl):

    def __init__(self, parent):
    
        wx.ListCtrl.__init__(self, 
                             parent,
                             style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
                            
                        
                        
        self.AppendColumn("Preferences")
        self.AppendColumn("About")
        self.AppendColumn("Setting")
        
        options = [("startup", "Run application on login", 0),
                   ("autoconnect", "Connect on application startup", 0),
                   ("autoreconnect", "Attempt to autoreconnect on loss of connection", 0),
                   ("onclose" , "Action on close button", ""),
                   ("onminimise", "Action on minimise button", ""),
                   ("allowresize", "Allow window resize", 0),
                   ("recentlyused", "Number of recently used items. \nIf -1: Infinity, If 0: Recently Used option is hidden", 10),
                   ("icon theme", "Show adapters", 0)]
                
        for op in options:
            self.Append(op)
            
class Preferences(BasePanel):
    """ navigate different """
    
    def __init__(self, parent):
        BasePanel.__init__(self, 
                           parent)
                            
        sizer = wx.BoxSizer(wx.VERTICAL)
        list = PreferencesList(self)
        sizer.Add(list, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)