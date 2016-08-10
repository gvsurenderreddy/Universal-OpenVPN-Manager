import wx


#System Colours
DEFAULTFONT = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
SYSCOLOURHIGHLIGHT = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT) #selected item background

class CustomTextCtrl(wx.TextCtrl):
    """
    A custom class that replicates some of the functionalities of wx.SpinCtrl
    """
    
    def __init__(self, 
                 parent, 
                 value=None, 
                 id=wx.ID_ANY,
                 pos=wx.DefaultPosition, 
                 size=wx.DefaultSize, 
                 style=wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.TE_RICH2|wx.TE_LEFT,
                 validator=wx.DefaultValidator,
                 name="CustomTextCtrl"):
        
        wx.TextCtrl.__init__(self, 
                             parent, 
                             id,
                             value,
                             pos, 
                             size, 
                             style, 
                             validator,
                             name)
                             
       
    def GetEditorType():  
        return "control"
                
    def GetEditorName():        
        return "CustomTextCtrl"
       