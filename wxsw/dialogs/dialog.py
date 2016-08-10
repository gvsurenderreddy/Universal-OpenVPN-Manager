import wx

class CustomDialog(wx.Dialog):
    # class CustomSpinCtrl(wx.Window):
    """
    A custom class that replicates some of the functionalities of wx.SpinCtrl
    """
    
    def __init__(self,
                 parent, 
                 title=""):
        
        wx.Dialog.__init__(self,
                           parent, 
                           id=wx.ID_ANY,
                           title=title,
                           pos=wx.DefaultPosition, 
                           size=wx.DefaultSize, 
                           style=wx.DEFAULT_DIALOG_STYLE,
                           name=wx.DialogNameStr)
        
        
        # self.ShowModal()
        
        
    def ShowModal(self):
        super(CustomDialog, self).ShowModal() 
        return self.GetValue()
        
    def SetValueString(self, value=0):
        """ choose the GetValue parser return value """
        valueStr = {0: ["fullpath"],                
                    1: ["file","path"],
                    3: ["path","file"],
                    4: ["file"]}                   
    
        self._valueStr = valueStr[value]
        
    def SetFocus(self):
        # super(CustomFileDialog, self).SetFocus()
        pass
        
    def GetEditorType():        
        return "CustomDialog"
      
    def GetEditorName():        
        return "dialog"
                
    def GetValue(self):
        """
        Returns the time h,m,s joined by separator
        """
        return None
    
        