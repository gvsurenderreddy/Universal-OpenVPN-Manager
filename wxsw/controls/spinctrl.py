import wx


#System Colours
DEFAULTFONT = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
SYSCOLOURHIGHLIGHT = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT) #selected item background


class CustomSpinCtrl(wx.Control):
# class CustomSpinCtrl(wx.Window):
    """
    A custom class that replicates some of the functionalities of wx.SpinCtrl
    """
    
    def __init__(self, 
                 parent, 
                 value=None, 
                 separator=":",
                 range=(0,None),
                 id=wx.ID_ANY,
                 pos=wx.DefaultPosition, 
                 size=wx.DefaultSize, 
                 style=wx.TE_PROCESS_TAB|wx.WANTS_CHARS,
                 validator=wx.DefaultValidator,
                 name="CustomSpinCtrl",
                 leftDelim="",
                 rightDelim=""):
        
        wx.Control.__init__(self, 
                            parent, 
                            id,
                            pos, 
                            size, 
                            style, 
                            validator,
                            name)
        
        self._delimiter = (str(leftDelim), str(rightDelim))
        self.SetRange(range)
        self._separator = separator
        if value is None:            
            self.SetValue(self._separator.join([str(x) for x in [0,0,0]]))
        else:    
            self.SetValue(value)
        
        self._spacing = 3 #spacing between check bitmap and label
        self._hasFocus = False        
        self._selectedItem = 0
        
        # Initialize the focus pen colour/dashes, for faster drawing later
        self.InitializeColours()
        
        # Ok, set the wx.Control label, its initial size (formerly known an
        # SetBestFittingSize), and inherit the attributes from the standard
        # wx.CheckBox
        self.SetInitialSize(size)
        self.InheritAttributes()

        # Bind the events related to our control: first of all, we use a
        # combination of wx.BufferedPaintDC and an empty handler for
        # wx.EVT_ERASE_BACKGROUND (see later) to reduce flicker
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        # detect position of mouse click
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)
        if wx.Platform == '__WXMSW__':
            # MSW Sometimes does strange things...
            self.Bind(wx.EVT_LEFT_DCLICK,  self.OnMouseClick)

        # We want also to react to keyboard keys, namely the
        # space bar that can toggle our checked state
        self.Bind(wx.EVT_CHAR, self.OnKeyUp)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyUp)
        
        self.Bind(wx.EVT_SET_FOCUS, self._OnDoubleClick )         ## defeat automatic full selection
        self.Bind(wx.EVT_KILL_FOCUS, self._OnDoubleClick )    ## run internal validator
        self.Bind(wx.EVT_LEFT_DCLICK, self._OnDoubleClick)  ## select field under cursor on dclick
        self.Bind(wx.EVT_RIGHT_UP, self._OnDoubleClick )    ## bring up an appropriate context menu
        # self.Bind(wx.EVT_KEY_DOWN, self__OnDoubleClick )        ## capture control events not normally seen, eg ctrl-tab.
        # self.Bind(wx.EVT_CHAR_HOOK, self._OnCharHook )               ## handle each keypress
        self.Bind(wx.EVT_TEXT, self._OnDoubleClick )         ## color control appropriately & keep
                                                            ## track of previous value for undo

        # Then, we react to focus event, because we want to draw a small
        # dotted rectangle around the text if we have focusall
        # This might be improved!!!
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
                
        
        bestWidth, bestHeight = self.DoGetBestSize()
        # self.SetSize(60,55)
        print(bestWidth, bestHeight)
        #fix the position
        spin = wx.SpinButton(self, pos=(bestWidth*2-2, 0), size=(-1,bestHeight))
        # spinDown = wx.SpinButton(self, pos=(-1, bestHeight/2))
        
    def GetEditorType():
        return "control"
        
    def GetEditorName():        
        return "CustomSpinCtrl"
        
    def _OnDoubleClick(self, e):
        pass
        
    def _OnCharHook(self, event):
        """ stop control from losing focus """
        pass
        
    def onTimer(self, evt):
        print ('Focused window:', wx.Window.FindFocus())
        
    def InitializeColours(self):
        """ Initializes the focus indicator pen. """

        textClr = self.GetForegroundColour()
        if wx.Platform == "__WXMAC__":
            self._focusIndPen = wx.Pen(textClr, 1, wx.SOLID)
        else:
            self._focusIndPen  = wx.Pen(textClr, 1, wx.USER_DASH)
            self._focusIndPen.SetDashes([1,1])
            self._focusIndPen.SetCap(wx.CAP_BUTT)
        
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


    def DoGetBestSize(self):
        """
        Overridden base class virtual.  Determines the best size of the control
        based on the label size, the bitmap size and the current font.
        """
        value = self.GetValue()
        font = self.GetFont()
        separator = self.GetSeparator()
        if not font:
            # No font defined? So use the default GUI font provided by the system
            font = DEFAULTFONT

        # Set up a wx.ClientDC. When you don't have a dc available (almost
        # always you don't have it if you are not inside a wx.EVT_PAINT event),
        # use a wx.ClientDC (or a wx.MemoryDC) to measure text extents
        dc = wx.ClientDC(self)
        dc.SetFont(font)

        # Get the spacing between the check bitmap and the text
        spacing = self.GetSpacing()
        value_str = separator.join([str(n) for n in value])
        textWidth, textHeight = dc.GetTextExtent(value_str)
        # Ok, we're almost done: the total width of the control is simply
        # the sum of the bitmap width, the spacing and the text width,
        # while the height is the maximum value between the text width and
        # the bitmap width
        totalWidth = spacing + textWidth
        totalHeight = textHeight
                
        best = wx.Size(totalWidth, totalHeight)

        # Cache the best size so it doesn't need to be calculated again,
        # at least until some properties of the window change
        self.CacheBestSize(best)

        return best


    def AcceptsFocusFromKeyboard(self):
        """Overridden base class virtual."""

        # We can accept focus from keyboard, obviously
        # return False
        return False


    def AcceptsFocus(self):
        """ Overridden base class virtual. """

        # It seems to me that wx.CheckBox does not accept focus with mouse
        # but please correct me if I am wrong!
        return False        


    def HasFocus(self):
        """ Returns whether or not we have the focus. """

        # We just returns the _hasFocus property that has been set in the
        # wx.EVT_SET_FOCUS and wx.EVT_KILL_FOCUS event handlers.
        return self._hasFocus


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
        
    def GetDefaultAttributes(self):
        """
        Overridden base class virtual.  By default we should use
        the same font/colour attributes as the native wx.CheckBox.
        """
        
        return wx.CheckBox.GetClassDefaultAttributes()


    def ShouldInheritColours(self):
        """
        Overridden base class virtual.  If the parent has non-default
        colours then we want this control to inherit them.
        """
        
        return True


    def SetSpacing(self, spacing):
        """ Sets a new spacing between the check bitmap and the text. """

        self._spacing = spacing

        # The spacing between the check bitmap and the text has changed,
        # so we must recalculate our best size and refresh ourselves.
        self.InvalidateBestSize()
        self.Refresh()


    def GetSpacing(self):
        """ Returns the spacing between the check bitmap and the text. """
        
        return self._spacing
    

    def GetValue(self, value=None):
        """
        Returns the state of CustomCheckBox, True if checked, False
        otherwise.
        """
        left, right = self._delimiter
        value = left + self._separator.join([str(val) for val in self._value]) + right
        return value
    
    def GetSeparator(self):
        """
        Returns the state of CustomCheckBox, True if checked, False
        otherwise.
        """
        
        return self._separator
     
    def SetRange(self, range):
        """
        Set minimum and maximum value. A value of None has no limit.  
        """
        min, max = range
        if min:
            int(min)
            
        if max:
            int(max)
        
        self._range = (min, max)   
        
    def GetRange(self):
        """
        Set minimum and maximum value. A value of None has no limit.  
        """
        
        return self._range   
        
    def SetValue(self, value):
        """
        Sets the CustomCheckBox to the given state. This does not cause a
        wx.wxEVT_COMMAND_CHECKBOX_CLICKED event to get emitted.
        """  
        #Check numbers are all int 
        try:
            value.lower()
            value = value.split(self._separator) 
            
            if isinstance(value, list):         
                for num in value: 
                    int(num)   
        except:
            pass
            
        self._value = value
        
        # Refresh: the value has changed        
        self.Refresh()


    def OnKeyUp(self, event):
        """ Handles the wx.EVT_KEY_UP event. """
        self.SetFocus()
        
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            # # The spacebar has been pressed: toggle our state
            self.Destroy()
            # # event.Skip()
            # return
            
        # if event.GetKeyCode() == wx.WXK_SPACE:
            # # The spacebar has been pressed: toggle our state
            # self.SendCheckBoxEvent()
            # # event.Skip()
            # return
        
        selection = self.GetSelection()
        min, max = self.GetRange()
        value = self._value
        v = int(value[selection])
        print(v)
        if event.GetKeyCode() == wx.WXK_LEFT:
            if selection == 0:      
                return
            self.SetSelection(selection - 1)
            
        elif event.GetKeyCode() == wx.WXK_RIGHT:            
            if selection == len(value)-1:
                return
            self.SetSelection(selection + 1)
        
        elif event.GetKeyCode() == wx.WXK_UP: 
            if max is None:
                v += 1
            elif v >= max:
                v = max
            else:    
                v += 1
            value[selection] = v    
            self.SetValue(value)   
            
        elif event.GetKeyCode() == wx.WXK_DOWN:  
            if min is None:
                v -= 1
            elif v <= min:
                v = min
            else:    
                v -= 1        
            value[selection] = v
            self.SetValue(value)   
        
        else: 
            event.Skip()
        self.Refresh()                 


    def OnSetFocus(self, event):
        """ Handles the wx.EVT_SET_FOCUS event for CustomCheckBox. """
        self.SetFocus()

        # We got focus, and we want a dotted rectangle to be painted
        # around the checkbox label, so we refresh ourselves
        self.Refresh()


    def OnKillFocus(self, event):
        """ Handles the wx.EVT_KILL_FOCUS event for CustomCheckBox. """
        # return
        # self._hasFocus = False
        return
        # self.SetFocus()
        # We lost focus, and we want a dotted rectangle to be cleared
        # around the checkbox label, so we refresh ourselves        
        self.Refresh()

        
    def OnPaint(self, event):
        """ Handles the wx.EVT_PAINT event for CustomCheckBox. """

        # If you want to reduce flicker, a good starting point is to
        # use wx.BufferedPaintDC.
        dc = wx.BufferedPaintDC(self)

        # Is is advisable that you don't overcrowd the OnPaint event
        # (or any other event) with a lot of code, so let's do the
        # actual drawing in the Draw() method, passing the newly
        # initialized wx.BufferedPaintDC
        self.Draw(dc)


    def Draw(self, dc):
        """
        Actually performs the drawing operations, for the bitmap and
        for the text, positioning them centered vertically.
        """

        # Get the actual client size of ourselves
        width, height = self.GetClientSize()

        if not width or not height:
            # Nothing to do, we still don't have dimensions!
            return

        # Initialize the wx.BufferedPaintDC, assigning a background
        # colour and a foreground colour (to draw the text)
        backColour = self.GetBackgroundColour()
        backBrush = wx.Brush(backColour, wx.SOLID)
        dc.SetBackground(backBrush)
        dc.Clear()

        if self.IsEnabled():
            dc.SetTextForeground(self.GetForegroundColour())
        else:
            dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
            
        dc.SetFont(self.GetFont())

        # Get the text label for the checkbox, the associated check bitmap
        # and the spacing between the check bitmap and the text
        separator = self.GetSeparator()
        value = self._value
        spacing = self.GetSpacing()
        value_str = separator.join([str(n) for n in value])
        # Measure the text extent and get the check bitmap dimensions
        textWidth, textHeight = dc.GetTextExtent(value_str)
        separatorwidth, separatorheight = dc.GetTextExtent(separator)
        
        # Measure our label        
        textWidth, textHeight = dc.GetTextExtent(value_str)
        
        self.textWidths = []
        selection = self.GetSelection()
        items = value_str.split(self._separator)
        for x in items:
            w, h = dc.GetTextExtent(x)            
            self.textWidths.append(w)
          
        dc.SetPen(wx.Pen(SYSCOLOURHIGHLIGHT,style=wx.TRANSPARENT))
        dc.SetBrush(wx.Brush(SYSCOLOURHIGHLIGHT, wx.SOLID))
        if selection == 0:
            dc.DrawRectangle(spacing, 0, self.textWidths[0], height)
        else:
            print(self.GetSelection())
            offset = spacing + (separatorwidth*selection) + sum(self.textWidths[:selection])            
            dc.DrawRectangle(offset, 0, self.textWidths[selection], height)
            
        print(self.textWidths)   
        # Position the text centered vertically
        textXpos = self._spacing
        textYpos = (height - textHeight)/2

        dc.DrawText(value_str, textXpos, textYpos)

        # Let's see if we have keyboard focus and, if this is the case,
        # we draw a dotted rectangle around the text (Windows behavior,
        # I don't know on other platforms...)
        if self.HasFocus():
            # Yes, we are focused! So, now, use a transparent brush with
            # a dotted black pen to draw a rectangle around the text
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetPen(self._focusIndPen)
            
            # dc.DrawRectangle(textXpos, textYpos, textWidth, textHeight)
            
            # draw a rectangle outline
            dc.DrawRectangle(9, 15, width, height)

    def OnEraseBackground(self, event):
        pass
        

    def OnMouseClick(self, event):
        """ Handles the wx.EVT_LEFT_DOWN event for CustomCheckBox. """
        return
        if not self.IsEnabled():
            # Nothing to do, we are disabled
            return

        self.SendCheckBoxEvent()
        # event.Skip()


    def SendCheckBoxEvent(self):
        """ Actually sends the wx.wxEVT_COMMAND_CHECKBOX_CLICKED event. """
        
        # This part of the code may be reduced to a 3-liner code
        # but it is kept for better understanding the event handling.
        # If you can, however, avoid code duplication; in this case,
        # I could have done:
        #
        # self._checked = not self.IsChecked()
        # checkEvent = wx.CommandEvent(wx.wxEVT_COMMAND_CHECKBOX_CLICKED,
        #                              self.GetId())
        # checkEvent.SetInt(int(self._checked))
        if self.IsChecked():

            # We were checked, so we should become unchecked
            self._checked = False
            
            # Fire a wx.CommandEvent: this generates a
            # wx.wxEVT_COMMAND_CHECKBOX_CLICKED event that can be caught by the
            # developer by doing something like:
            # MyCheckBox.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
            checkEvent = wx.CommandEvent(wx.wxEVT_COMMAND_CHECKBOX_CLICKED,
                                         self.GetId())
            
            # Set the integer event value to 0 (we are switching to unchecked state)
            checkEvent.SetInt(0)
        else:

            # We were unchecked, so we should become checked
            self._checked = True

            checkEvent = wx.CommandEvent(wx.wxEVT_COMMAND_CHECKBOX_CLICKED,
                                         self.GetId())

            # Set the integer event value to 1 (we are switching to checked state)
            checkEvent.SetInt(1)

        # Set the originating object for the event (ourselves)
        checkEvent.SetEventObject(self)

        # Watch for a possible listener of this event that will catch it and
        # eventually process it
        self.GetEventHandler().ProcessEvent(checkEvent)

        # Refresh ourselves: the bitmap has changed
        self.Refresh()

