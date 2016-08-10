import wx

class CustomTextEntryDialog(wx.TextEntryDialog):
    # class CustomSpinCtrl(wx.Window):
    """
    A custom class that replicates some of the functionalities of wx.SpinCtrl
    """
    
    def __init__(self,
                 parent, 
                 message="",
                 caption="",
                 value=""):
        
        wx.TextEntryDialog.__init__(self,
                                   parent, 
                                   message=message,
                                   caption=caption,
                                   value=value,
                                   pos=wx.DefaultPosition, 
                                   style=wx.TextEntryDialogStyle)
        
        
        # self.ShowModal()
        
    def ShowModal(self):
        super(CustomTextEntryDialog, self).ShowModal() 
        return self.GetValue()
        
    def GetEditorType():  
        return "dialog"
                
    def GetEditorName():
        return "CustomTextEntryDialog"
        
    def GetValue(self):
        return super(CustomTextEntryDialog, self).GetValue() 