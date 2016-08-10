# -*- coding: utf-8 -*-
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
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wxsw.listctrl import CustomEditListCtrl

SIDEBARFONT = wx.Font(pointSize = 12, family = wx.DEFAULT,
                       style = wx.NORMAL, weight = wx.NORMAL,
                       faceName = 'Consolas')
 
OUTPUTFONT = wx.Font(pointSize = 10, family = wx.DEFAULT,
                       style = wx.NORMAL, weight = wx.NORMAL,
                       faceName = 'Consolas')
                       
OUTPUTBGCOLOUR = "black" 
OUTPUTFGCOLOUR = "white" 
OUTPUTMESSAGEFGCOLOUR = "green" 
OUTPUTERRORFGCOLOUR = "red" 

CMDOUTPUTFONT = wx.Font(pointSize = 10, family = wx.DEFAULT,
                       style = wx.NORMAL, weight = wx.NORMAL,
                       faceName = 'Consolas')                       
CMDOUTPUTBGCOLOUR = "white" 
CMDOUTPUTFGCOLOUR = "blue" 
CMDOUTPUTMESSAGEFGCOLOUR = "green" 
CMDOUTPUTERRORFGCOLOUR = "red" 

class BaseListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):

    def __init__(self):
        pass
        
class BaseEditListCtrl(CustomEditListCtrl, ListCtrlAutoWidthMixin):

    def __init__(self):
        pass
        
class BasePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, 
                          parent)