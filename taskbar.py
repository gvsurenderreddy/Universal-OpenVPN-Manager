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
import wx.adv

class TaskBarIcon(wx.adv.TaskBarIcon):

    def __init__(self):
    
        super(TaskBarIcon, self).__init__()
        #self.SetIcon("icon.png")
        # self.Bind(wx.EVT_TASKBAR_LEFT, self.OnTaskBarLeft)
        #self.CreatePopupMenu()
        
    def CreatePopupMenu(self):
        menu = wx.Menu()
        #create_item(menu, 'Say Hello', self.on_hello)
        menu.AppendSeparator()
        #create_item(menu, 'Exit', self.on_exit)
        return menu

    def SetIcon(self, path):
        icon = wx.Icon(wx.Image(path))
        self.SetIcon(icon, "")

    def OnTaskBarLeft(self, event):
        print('Tray icon was left-clicked.')

    def on(self, event):
        print('Hello, world!')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)