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
import subprocess
import time
from os import walk
import os
import admin
import sys

from commandflags import Flags
from preferences import Preferences
from configs import Configs
from sidebar import Sidebar

import multiprocessing as mp

from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

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


settings = "config.ini"
exe = "\"c:/Program Files/OpenVPN/bin/openvpn.exe\""
exe = "\"c:/Program Files/OpenVPN/bin/openvpn-gui\""
reconnect = "0"
lastconnection = "0"
                
try:
    with open(settings,'r') as file:  
        list = file.read().splitlines() 
        exe,CONFIGPATH,reconnect,lastconnection = list
        print(exe,CONFIGPATH,reconnect,lastconnection)
except:
    pass
    # with open(settings,'w') as file:
       # print(" writing new settings file ")
       # file.write(exe)
       # file.write("\n")
       # file.write(configPath) 
       # file.write("\n")
       # file.write(reconnect)
       # file.write("\n")
       # file.write(lastconnection)
 
def UpdateConfig(rec=None,lastconn=None):    
    if rec:
        reconnect = "1"    
    else:
        reconnect = "0"  
    if lastconn:
        lastconnection = lastconn
    else:   
        lastconnection = "0"
    list = [exe,configPath,reconnect,lastconnection]                
    with open(settings,'w') as file:         
        for n in list:
            file.write(n) 
            file.write("\n") 
        
        
class Output(wx.ListCtrl, ListCtrlAutoWidthMixin):
    """ multiline text control for displaying output """
    
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, 
                             parent,
                             style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        ListCtrlAutoWidthMixin.__init__(self)
        self.AppendColumn("Time")
        self.AppendColumn("Status")        
        self.AppendColumn("Message")
        
        
        self.SetFont = OUTPUTFONT
        self.SetBackgroundColour(OUTPUTBGCOLOUR)
        self.SetForegroundColour(OUTPUTFGCOLOUR)
        
        pub.subscribe(self.PubAppendText, "PubAppendText")                
        pub.subscribe(self.PubRunCmd, "PubRunCmd")   

        #catch important messages or errors   
        self.important = ["Enter Auth Username:Options error: --auth-user-pass fails with",
                          "Enter Auth Username:"]
        self.messages = ["Initialization Sequence Completed",
                         "Successful ARP Flush on interface",]
        self.errors = ["frag ttl expired" ] #express vpn : unstable connection? change protocol?
        self.ignore = ["Options error: Please correct these errors."]                
        
    def PubRunCmd(self, msg):        
        param = msg.data 
        if param == "--config":
            os.chdir("c:/")
            print(os.getcwd())
            # print(os.system("dir"))  
            admin.run_as_admin([""])
            time.sleep(2)
            p = subprocess.Popen("openvpn.exe --config uk.ovpn --daemon", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # SubCall("openvpn.exe --config uk.ovpn")
        else:                    
            p = subprocess.Popen("openvpn.exe " + param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            pub.sendMessage("PubAppendText", out)  
        
    def PubAppendText(self, msg):
        try:
            text = msg.data.decode("utf8")
        except:
            text = msg.data
        
        hasIgnore = [ig for ig in self.ignore if ig in text]
        if hasIgnore:
            item = self.Append(["", "", text])
            self.SetItemTextColour(item, "yellow")
            return
            
        #try to catch important messages early
        hasImportant = [imp for imp in self.important if imp in text]
        if hasImportant:
            item = self.Append(["", "!", text])
            self.SetItemTextColour(item, "red")
            return
            
        #here we split the date from the log message
        text_list = text.split(" ")
        for n, s in enumerate(text_list):
            try:
                int(text_list[n][-1])
                try:
                    int(text_list[n+1][0])
                except:
                    text_str = " ".join(text_list[n+1:])
                    date = " ".join(text_list[:n+1])
                    break
            except:        
                continue
        
        
        try: 
            hasMessage = [message for message in self.messages if message in text_str]
            hasError = [err for err in self.errors if err in text_str]
            
            if hasMessage:
                item = self.Append([date, ":)", text_str])
                self.SetItemTextColour(self.GetItemCount()-1, OUTPUTMESSAGEFGCOLOUR)
            elif hasMessage:
                item = self.Append([date, "Error", text_str])
                self.SetItemTextColour(item, OUTPUTERRORFGCOLOUR)
                self.Focus() #focus on error message
            else:
                item = self.Append([date, "", text_str])
                self.SetItemTextColour(item, OUTPUTFGCOLOUR)
            print(hasMessage)
            self.EnsureVisible(self.GetItemCount()-1) #auto scroll
        except:
            print (text)
        
        self.SetForegroundColour(OUTPUTFGCOLOUR)
        

        
class Main(wx.Frame):
    """ 
    
    #------------------------------#
     title
    #------------------------------#    
    #            |                 #         
    # sidebar    |                 #         
    #            |                 #         
    #            |                 # 
    #            |                 #         
    #            |                 # 
    #            |                 #         
    #            |                 #       
    #------------------------------# <- splitter
    # output            | controls #     
    #                   |          # 
    #------------------------------#
    
    """
    
    def __init__(self):
        wx.Frame.__init__(self, 
                          None,           
                          title='OpenVPN Connector')
        
        self.CreateStatusBar()
        #Create multi-panel UI
        self.mainpanel = wx.Panel(self)
        mainsizer = wx.BoxSizer(wx.VERTICAL)   
        splitter = wx.SplitterWindow(self.mainpanel) #horizontal
        subsplitter = wx.SplitterWindow(splitter) #vertical
        self.subsplitter = subsplitter
        # top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # top_panel = wx.Panel(subsplitter)
          
        self.sidebar = Sidebar(subsplitter)
        sidebarMenu = [("Configs", Configs),
                       ("Command Flags", Flags),
                       ("Preferences", Preferences)]
        
        self.subpanels = {} 
        for name, pnl in sidebarMenu:
            panel = pnl(self.subsplitter)            
            panel.Hide()
            # top_sizer.Add(panel, 2, wx.ALL|wx.EXPAND, 2)
            self.subpanels[name] = panel
        self.subpanels["Configs"].Show()
        # self.currentpanel = self.subpanels["Configs"]
        # top_panelthe.SetSizer(top_sizer)
        
        #the bottom_sizer contains buttons and controls
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)   
        bottom_panel = wx.Panel(splitter)
        
        txt = Output(bottom_panel)
        
        control_grid = wx.GridSizer(cols=3)
        for label in ["Clear","Export","Reconnect","Disconnect","Force Reconnect"]:
            btn = wx.Button(bottom_panel, label=label)
            btn.Bind(wx.EVT_BUTTON, self.OnButton)
            control_grid.Add(btn, 0, wx.ALL|wx.EXPAND, 2)
        # self.text = wx.StaticText(bottom_panel,label="Connection: None")
        # bottom_sizer.Add(self.text, 5, wx.ALL|wx.EXPAND, 2)        
        
        bottom_sizer.Add(txt, 2, wx.ALL|wx.EXPAND, 2)
        bottom_sizer.Add(control_grid, 1, wx.ALL|wx.EXPAND, 2)
        bottom_panel.SetSizer(bottom_sizer)
      
        # mainsizer.Add(top_panel, 3, wx.ALL|wx.EXPAND, 0)
        # mainsizer.Add(bottom_panel, 1, wx.ALL|wx.EXPAND, 0)
        
        subsplitter.SplitVertically(self.sidebar, self.subpanels["Configs"])
        subsplitter.SetSashGravity(0.3)
        splitter.SplitHorizontally(subsplitter, bottom_panel)
        splitter.SetSashGravity(0.7)
        
        # mainsizer.Add(subsplitter, 1, wx.ALL|wx.EXPAND, 0)
        mainsizer.Add(splitter, 1, wx.ALL|wx.EXPAND, 5)
        self.mainsizer = mainsizer
        self.mainpanel.SetSizer(mainsizer)  
        self.mainsizer.Fit(self)
        self.SetMinSize(self.GetBestSize())
        self.Show()
        
        # if reconnect == "1":
            # self.on.Disable()
            # if lastconnection != "0":
                # print("connecting to last used connection")
                # SubCall(lastconnection)
        # else:
            # self.off.Disable()
            
        #pub-sub
        pub.subscribe(self.DoConnect, "DoConnect")
        pub.subscribe(self.PubSubChangeMainPanel, "PubSubChangeMainPanel")
        
        #Timers
        self.log_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnLogTimer, self.log_timer)
        self.log_read = 0
                
        # with open("c:\openvpn.log", "w+") as log:
            # print(" creating new log file ")
            # log.close()
            
    def OnLogTimer(self, event):
        with open("c:\openvpn.log", "r") as log:
            read = 0
            for line in log:
                if self.log_read > read:
                    read += 1
                    continue
                pub.sendMessage("PubAppendText", line)
                self.log_read += 1
        
        # self.log_timer.Stop()
                
    def OnToolBarButton(self, e): 
        label = e.GetEventObject().GetLabel()
        if label == "close":
            exit()
        
    def OnReconnect(self, e): 
        label = e.GetEventObject().GetLabel()
        if label == "Reconnect On":
            self.on.Disable()
            self.off.Enable()
            UpdateConfig(rec=True)
        elif label == "Reconnect Off":
            self.off.Disable()
            self.on.Enable()
            UpdateConfig(rec=None)

    def OnButton(self, e): 
        label = e.GetEventObject().GetLabel()
        # exe = "openvpn"
        cmd = exe + " --config \"" + configPath + label + ".ovpn\""
        cmd = exe + " --connect \"" + configPath + label + ".ovpn\""
        cmd = exe + " --connect \"" + label + ".ovpn\""
        self.SetStatusText(cmd)  
        self.jobs = []
        self.DoConnect(cmd)
    
    def PipeOutput(self, pipe):
        stdin, out, err = pipe.communicate()
        pub.sendMessage("PubAppendText", out)
        print(p)
        self.SetStatusText("stdin:"+str(stdin))
        p.communicate(input='data_to_write')[0]
        
    def RunCmd(self, cmd):
        admin.RunAsAdmin(self.queue, cmd)
        
    def PubSubChangeMainPanel(self, msg):
        """ sidebar selection has changed, therefore we change the panel """
      
        item_txt = msg.data
        if item_txt in self.subpanels:
            show_list = item_txt
        else:
            show_list = "Configs"
            
        for name in self.subpanels: 
            if show_list == name:
                continue
            self.subpanels[name].Hide()
                
        if self.subpanels[show_list].IsShown() is False:
            print(self.subpanels[show_list].IsShown())
            # self.top_sizer.Fit(self.subpanels[show_list])
            # self.subpanels[show_list].Fit()
            # self.subpanels[show_list].SetSize(self.top_panel.GetClientSize()) #fits size on layout
            self.subpanels[show_list].Fit()
            self.subpanels[show_list].Show()
          
        if show_list == "Configs":
            pass
        
        # self.subsplitter.Unsplit(self.subsplitter.GetWindow2())
        self.subsplitter.ReplaceWindow(self.subsplitter.GetWindow2(), self.subpanels[show_list])
        # self.main_panels[show_list].Fit()
        # self.Refresh()
        # self.mainsizer.Fit(self)
        # self.top_panel.SetSizer(self.top_sizer)
        # self.top_sizer.Add(self.subpanels[show_list], 1, wx.ALL |wx.EXPAND)
        # self.SetSize(self.GetBestSize())
        self.Layout()
        # self.Update()
        
        
        
        
    def DoConnect(self, msg):
        """ method for connecting to a vpn """
        
        # first stop any running openvpn processes
        killcmd = ["taskkill.exe", "/f /im openvpn-gui.exe"]
        killcmd2 = ["taskkill.exe", "/f /im openvpn.exe"]
        admin.RunAsAdmin(cmdLine=killcmd)
        admin.RunAsAdmin(cmdLine=killcmd2)
        
        time.sleep(0.5)      
        
        #now deal with config
        config, path = msg.data
        print        (msg.data)
        fullpath = path + config + ".ovpn"
        fullpath = "\"" + fullpath + "\"" #enclose with quotes because of potential spaces in str
        
        # self.cmd = '"c:/Program Files/OpenVPN/bin/openvpn-gui" --connect "uk.ovpn"'
        # path =  "c:\\Program Files\\OpenVPN\\config\\"
        
        flags = "--log-append c:/openvpn.log" 
        flags += " --config " + fullpath
        openvpn = "openvpn.exe"
        cmd = [openvpn, flags]
        print("cmd",cmd)
        # self.cmd = '"c:/Program Files/OpenVPN/bin/openvpn-gui" --connect "uk.ovpn"'
        # self.cmd = "--connect-retry-max 5 --dev \"Ethernet 2\" --config \"c:\\Program Files\\openvpn\\config\\uk.ovpn\""        
        # if not hasattr(self, "queue"):
        self.queue = mp.Queue()
        print("queue!", self.queue)
        # parent_conn, child_conn = mp.Pipe()
        # m = mp.Process(target=test, args=(child_conn, cmd,))
        
        # m = mp.Process(target=admin.RunAsAdmin, args=(self.queue, cmd,))
        m = mp.Process(target=self.RunCmd, args=(cmd,))
        
        # m = mp.Process(target=self.RunCmd, args=(None,cmd,))
        m.start()
        print(self.queue.get())
        # m.join()
        # print (parent_conn.recv()) 
        
        # while True:
        # admin.RunAsAdmin(cmd)
        if not self.log_timer.IsRunning():
            self.log_timer.Start(5)
        # print (self.queue.get()) 
        # self.queue.close()
        
        
        self.SetFocus()

class ErrorStartup(wx.Dialog):

    def __init__(self):
        wx.Dialog.__init__(self, 
                           parent=None, 
                           title="Error: cannot be run as admin")
        self.Centre()
        self.Show()
        
if __name__ == '__main__':
    app = wx.App(False)
    if admin.IsUserAdmin():
        ErrorStartup()
    else:  
        Main()
    #TaskBarIcon().Show()
    app.MainLoop()