import wx
from wx.adv import TimePickerCtrl

class CustomTimePickerCtrl(TimePickerCtrl):
    # class CustomSpinCtrl(wx.Window):
    """
    A custom class that replicates some of the functionalities of wx.SpinCtrl
    """
    
    def __init__(self,
                 parent, 
                 value=None,
                 name="CustomTimePickerCtrl"):            
        
        TimePickerCtrl.__init__( self,
                                 parent,
                                 id=wx.ID_ANY, 
                                 dt=wx.DefaultDateTime,
                                 pos=wx.DefaultPosition, 
                                 size=wx.DefaultSize,
                                 style=wx.adv.TP_DEFAULT,
                                 validator=wx.DefaultValidator,
                                 name="CustomTimePickerCtrl")  
                                 
        if value is None:
            # self.SetValue([0,0,0])
            pass #use current date
        else:    
            self.SetValue(value)        
   
    def GetEditorType():  
        return "control"
                
    def GetEditorName():        
        return "CustomTimePickerCtrl"
        
        
    def SetFont(self, font):
        """
        Sets the CustomCheckBox text font and updates the control's size to
        exactly fit the label plus the bitmap.
        """
        
        wx.Control.SetFont(self, font)

        # The font for text label has changed, so we must recalculate our best
        # size and refresh ourselves.        
        self.InvalidateBestSize()
        self.Refresh()

    def SetForegroundColour(self, colour):
        """ Overridden base class virtual. """

        wx.Control.SetForegroundColour(self, colour)

        # We have to re-initialize the focus indicator per colour as it should
        # always be the same as the foreground colour
        self.InitializeColours()
        self.Refresh()


    def SetBackgroundColour(self, colour):
        """ Overridden base class virtual. """

        wx.Control.SetBackgroundColour(self, colour)

        # We have to refresh ourselves
        self.Refresh()

    def Enable(self, enable=True):
        """ Enables/Disables CustomCheckBox. """

        wx.Control.Enable(self, enable)

        # We have to refresh ourselves, as our state changed        
        self.Refresh()

    def SetSelection(self, value):              
        self._selectedItem = value
        
    def GetSelection(self):   
        return self._selectedItem
   
    def GetValue(self, value=None):
        """
        Returns the time h,m,s joined by separator
        """
        pass
        return self._value
    
    def GetSeparator(self):
        """
        Returns the state of CustomCheckBox, True if checked, False
        otherwise.
        """
        
        return self._separator
     
        
    def SetValue(self, value):
        """
        Sets the CustomCheckBox to the given state. This does not cause a
        wx.wxEVT_COMMAND_CHECKBOX_CLICKED event to get emitted.
        """  
        hms = value.split(":")            
        self._value = value
        h,m,s = [int(x) for x in hms]
        self.SetTime(h, m, s)
        
