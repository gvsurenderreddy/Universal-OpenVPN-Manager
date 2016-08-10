import wx


#System Colours
DEFAULTFONT = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
SYSCOLOURHIGHLIGHT = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT) #selected item background


class CustomComboBox(wx.ComboBox):
    """
    A custom class that replicates some of the functionalities of wx.SpinCtrl
    """
    
    def __init__(self, 
                 parent, 
                 id=wx.ID_ANY, 
                 value="", 
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 choices=[], 
                 style=wx.CB_READONLY|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.TE_RICH2, 
                 validator=wx.DefaultValidator,
                 name="CustomComboBox"):
        
        wx.ComboBox.__init__(self, 
                             parent, 
                             id,
                             value, 
                             pos,
                             size, 
                             choices, 
                             style, 
                             validator,
                             name)
        
    def GetEditorType():  
        return "control"
                
    def GetEditorName():        
        return "CustomComboBox"
        

