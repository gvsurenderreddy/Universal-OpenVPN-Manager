import wx

class CustomFileDialog(wx.FileDialog):
    # class CustomSpinCtrl(wx.Window):
    """
    A custom class that replicates some of the functionalities of wx.SpinCtrl
    """
    
    def __init__(self,
                 parent, 
                 valueStr=0, 
                 message=wx.FileSelectorPromptStr):
        
        wx.FileDialog.__init__(self,
                               parent, 
                               message,
                               defaultDir="", 
                               defaultFile="",
                               wildcard=wx.FileSelectorDefaultWildcardStr, 
                               style=wx.FD_DEFAULT_STYLE|wx.FD_FILE_MUST_EXIST,
                               pos=wx.DefaultPosition, 
                               size=wx.DefaultSize, 
                               name=wx.FileDialogNameStr)
        
        # self._valueStr = 0
        self.SetValueString(valueStr)
        # self.ShowModal()
        
    def ShowModal(self):
        super(CustomFileDialog, self).ShowModal() 
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
        return "dialog"
                
    def GetEditorName():        
        return "CustomFileDialog"
        
    def GetValue(self):
        """
        Returns the time h,m,s joined by separator
        """
        file = self.GetFilename()
        fullpath = self.GetPath()
        path = fullpath[:fullpath.index(file)]
        filedict = {"file":file,
                    "fullpath":fullpath,
                    "path":path,}
                            
        value = []
        for s in self._valueStr:
            value.append(filedict[s])
        
        value = ",".join(value)
        return value
    
        