"""
<PyRoboTool Alarm & Countdown Timer - execute tasks on scheduled time>
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
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import wx
from bisect import bisect

from wxsw.mixins.listctrl import *
from wxsw.controls.spinctrl import CustomSpinCtrl 

class CustomEditListCtrl(wx.ListCtrl, CustomEditMixin):
    
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES)
        
        CustomEditMixin.__init__(self)
               