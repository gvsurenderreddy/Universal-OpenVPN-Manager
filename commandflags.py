# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:30:17 2016

Command Flags panel - contains list of command flags/parameters

Default usage - kept hidden from sidebar. 

"""

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

from base import *
import subprocess

class CommandOutput(wx.TextCtrl):
    """ multiline text control for displaying output """
    
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, 
                             parent,
                             style=wx.TE_MULTILINE)
                             
        self.SetFont = CMDOUTPUTFONT
        self.SetBackgroundColour(CMDOUTPUTBGCOLOUR)
        self.SetForegroundColour(CMDOUTPUTFGCOLOUR)
        
        #catch important messages or errors   
        self.important = ["Enter Auth Username:Options error: --auth-user-pass fails with",
                          "Enter Auth Username:"]
        self.messages = ["Initialization Sequence Completed",
                         "Successful ARP Flush on interface",]
        self.errors = ["frag ttl expired" ] #express vpn : unstable connection? change protocol?
        self.ignore = ["Options error: Please correct these errors."]                
            
        
class FlagsList(wx.ListCtrl, ListCtrlAutoWidthMixin):
    """ populates list with openvpn commandline arguments """
    
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, 
                             parent,
                             style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        
        ListCtrlAutoWidthMixin.__init__(self)
        
        self.AppendColumn("cmd")
        self.AppendColumn("about")
        
        options = [("--version", "Show copyright and version information."),
                   ("--config" , "Read configuration options from file."),
                   ("--daemon", "Become a daemon after initialization. The " 
                                + "optional 'name' parameter will be passed "
                                + "as the program name to the system logger."),
                   ("--show-adapters", "show adapters "),
                   ("--show-tls", "")]  
                       
        for op in options:            
            self.Append(op)

class Flags(BasePanel):
    """ navigate different """
    
    def __init__(self, parent):
        BasePanel.__init__(self, 
                           parent)
                           
        sizer = wx.BoxSizer(wx.HORIZONTAL)                    
        splitter = wx.SplitterWindow(self)
        self.output = CommandOutput(splitter)
        self.list = FlagsList(splitter)
        
        splitter.SplitHorizontally(self.output, self.list)
        splitter.SetSashGravity(0.5)
        sizer.Add(splitter, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)
        
        #Bindings
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
        
    def OnListItemActivated(self, event):
        e = event.GetIndex()
        
        param = self.list.GetItemText(e)     
        self.DoRunCmd(param)
        
    def DoRunCmd(self, param):        
        # param = msg.data 
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
            # pub.sendMessage("PubAppendText", out)
            self.output.AppendText("#")
            self.output.AppendText("-----"*5)
            self.output.AppendText("\n")
            self.output.AppendText(out)
            self.output.AppendText("-----"*5)
            self.output.AppendText("#")
            self.output.AppendText("\n")
            
    def AppendText(self, msg):
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