import wx
from wx.adv import DatePickerCtrl


class CustomDatePickerCtrl(DatePickerCtrl):
    # class CustomSpinCtrl(wx.Window):
    """
    A custom class that replicates some of the functionalities of wx.SpinCtrl
    """
    
    def __init__(self,
                 parent, 
                 value=None, 
                 name="CustomDatePickerCtrl"):
        
        DatePickerCtrl.__init__(self,
                                parent, 
                                id=wx.ID_ANY, 
                                dt=wx.DefaultDateTime,
                                pos=wx.DefaultPosition, 
                                size=wx.DefaultSize,
                                style=wx.adv.DP_DROPDOWN,
                                validator=wx.DefaultValidator,
                                name="CustomDatePickerCtrl")  
                                 
        
        if value is not None:
            self.SetValue(value)
            
    def GetEditorType():  
        return "control"
                
    def GetEditorName():  
        return "CustomDatePickerCtrl"
        
    def GetValue(self, value=None):
        """
        Returns the time h,m,s joined by separator
        """
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
        
        dmy = value.split("/")
        self._value = value
        d,m,y = [int(x) for x in dmy]
        date = wx.DateTime(day=d, month=m-1, year=y)
        
        super(CustomDatePickerCtrl, self).SetValue(date)