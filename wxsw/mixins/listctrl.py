
import wx
from bisect import bisect

from wxsw.controls.datepickerctrl import CustomDatePickerCtrl
from wxsw.controls.timepickerctrl import CustomTimePickerCtrl
from wxsw.controls.spinctrl import CustomSpinCtrl
from wxsw.controls.textctrl import CustomTextCtrl
from wxsw.controls.combobox import CustomComboBox

from wxsw.dialogs.dialog import CustomDialog
from wxsw.dialogs.filedialog import CustomFileDialog
from wxsw.dialogs.textentrydialog import CustomTextEntryDialog


class CustomEditMixin:
    """
    A mixin class that enables any text in any column of a
    multi-column listctrl to be edited by clicking on event given row
    and column. You close event text editor by hitting event ENTER key or
    clicking somewhere else on event listctrl. You switch to event next
    column by hiting TAB.

    To use event mixin you have to include it in event class definition
    and call event __init__ function::

    class TestListCtrl(wx.ListCtrl, CustomEditMixin):
        def __init__(self, parent, ID, pos=wx.DefaultPosition,
                     size=wx.DefaultSize, style=0):
            wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
            CustomEditMixin.__init__(self)
    """

    editor_colour_bg = wx.Colour(255,255,175) # yellow
    editor_colour_fg = wx.Colour(0,0,0)       # black

    def __init__(self):   
                
        #item values for which the editor will not be created        
        self._editorIgnore = []
        
        #Selected position
        self._selectedRow = None
        self._selectedCol = None      
        
        #Position of the editor
        self._editorRow = None
        self._editorCol = None
        
        self._editors = {}
        self._editorBind = {}
        
        # ListCtrl bindings
        self.Bind(wx.EVT_TEXT_ENTER, self._OnTextEnter)
        self.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftClick)  
        self.Bind(wx.EVT_LEFT_DCLICK, self.__OnLeftDoubleClick)
    
    def EditorIgnore(self, words):
        """ 
        append to a list of values which the editor should not be created.
        for example, to ignore invalid or n/a type values         
        """
        try:
            words.lower()
            words = [words]
        except:
            pass
            
        self._editorIgnore.extend(words)
        
        
    def SetupEditor(self, name, value=None):
        """ pass a custom control. Not implemented yet """
        self._editors[name] = [type, value]
     
    def SetupComboBox(self, name, choices, value=None):
        self._editors[name] = [CustomComboBox, choices, value]
   
    def SetupDatePickerCtrl(self, name, value=None):
        self._editors[name] = [CustomDatePickerCtrl, value]
      
    def SetupDialog(self, name, title=None, valueStr=""):
        """ pass a custom control """
        self._editors[name] = [CustomDialog, title]
        
    def SetupFileDialog(self, name, message=None, valueStr=0):
        """ pass a custom control """
        self._editors[name] = [CustomFileDialog, message, valueStr]

    def SetupSpinCtrl(self, name, value=None, separator="-"):
        self._editors[name] = [CustomSpinCtrl, value, separator]       
    
    def SetupTextCtrl(self, name, value=None):
        self._editors[name] = [CustomTextCtrl, value]
        
    def SetupTextEntryDialog(self, name, message=None, caption=None, value=None):
        """ pass a custom control """
        self._editors[name] = [CustomTextEntryDialog, message, caption, value]
        
    def SetupTimePickerCtrl(self, name, value=None):
        self._editors[name] = [CustomTimePickerCtrl, value]
        
    def BindEditor(self, editor, col, ifcol=None):
        """ 
        setup conditions for which the editor is created.        
         
        editor: name of the editor assigned in the SetupEditor() method
        col: has to match column name
        ifcol: if item text of a column on the same row
        
        ifcol = {columnname:value}
        ifrow = {row:value}
        
        """
        bind = {"col":col}
        if editor not in self._editors:
            raise Exception(ArgError, editor, "Editor does not exist")
        
        bind["ifcol"] = ifcol
        self._editorBind[editor] = bind
    
    
    def _OnTextEnter(self, event):
        self.CloseEditor(event)
        
    def _OnItemSelected(self, event):
        pass
        self._selectedRow = event.GetIndex()  
    
    def GetSelectedItem(self, event=None):
        """ return row and column position """
        
        return self._selectedRow, self._selectedCol
    
    def SetSelectedItem(self, event=None):
        x, y = event.GetPosition()
        row, flags = self.HitTest((x,y))
        
        # The following should really be done in the mixin's init but
        # the wx.ListCtrl demo creates the columns after creating the
        # ListCtrl (generally not a good idea). On the other hand,
        # doing this here handles adjustable column widths
        self._selectedCol_len = [0]
        col_len = 0
        for n in range(self.GetColumnCount()):
            col_len += self.GetColumnWidth(n)
            self._selectedCol_len.append(col_len)

        col = bisect(self._selectedCol_len, x+self.GetScrollPos(wx.HORIZONTAL)) - 1
        
        self._selectedRow = row
        self._selectedCol = col
        
    
    def __OnLeftClick(self, event):
        """ close editor if click position is different from editor position. """
        self.SetSelectedItem(event)
        row, col = self.GetSelectedItem()
                
        if row != self._editorRow or col != self._editorCol: 
            self.CloseEditor()     
        event.Skip()    
        
    def _CreateDialogEditor(self, editorLabel, editorName):
        selectedRow, selectedCol = self.GetSelectedItem()
        itemText = self.GetItem(selectedRow, selectedCol).GetText()
        _editor = self._editors[editorLabel][0]
        
        if editorName == "CustomDialog":
            title = self._editors[editorLabel][1]            
            
            if title is None:
                editor = _editor(self, title="")
            else:
                editor = _editor(self, title=title)
            
        elif editorName == "CustomTextEntryDialog":
            caption = self._editors[editorLabel][1]            
            message = self._editors[editorLabel][2]            
            value = self._editors[editorLabel][3]            
            
            if caption is None:
                caption = ""
            if message is None:
                message = ""
            if value is None:
                value = ""
            
            editor = _editor(self, caption=caption, message=message, value=value)            
            
        elif editorName == "CustomFileDialog":
            message = self._editors[editorLabel][1]
            valueStr = self._editors[editorLabel][2]
            
            if message is None:
                editor = _editor(self, valueStr=valueStr)
            else:
                editor = _editor(self, message=message, valueStr=valueStr)
            
            # destroy if another editor
            if hasattr(self, 'editor'):
                self.editor.Destroy() 
            self.editor = editor            
            self._editorRow = selectedRow
            self._editorCol = selectedCol
            self.CloseEditor()
            
    def _CreateControlEditor(self, editorLabel, editorName):
        selectedRow, selectedCol = self.GetSelectedItem()
        itemText = self.GetItem(selectedRow, selectedCol).GetText()
        _editor = self._editors[editorLabel][0]
        
        if editorName == "CustomComboBox":
            choices = self._editors[editorLabel][1]  
            value = self._editors[editorLabel][2]
            if value is None:
                if itemText in choices:
                    value = itemText                   
            else:
                value = choices[value]
                
            editor = _editor(self, choices=choices, value=value)
            editor.Bind(wx.EVT_COMBOBOX, self.CloseEditor)
        
        elif editorName == "CustomTextCtrl":
            value = self._editors[editorLabel][1]  
            if value is None:
                value = itemText                   
            else:
                value = str(value)
                
            editor = _editor(self, value=value)
            editor.Bind(wx.EVT_KILL_FOCUS, self.CloseEditor)
            editor.Bind(wx.EVT_CHAR, self.OnCharEditor)
            
        elif editorName == "CustomSpinCtrl":
            value = self._editors[editorLabel][1]
            if value is None:
                value = itemText
            else:
                value = None 
            separator = self._editors[editorLabel][2]     
            
            editor = _editor(self, value=value, separator=separator)
            editor.Bind(wx.EVT_KILL_FOCUS, self.CloseEditor)
            
        elif editorName == "CustomDatePickerCtrl":
            value = self._editors[editorLabel][1]
            if value is None:
                value = itemText
                
            editor = _editor(self, value=value)
            editor.Bind(wx.EVT_CHAR, self.OnCharEditor)
            
        elif editorName == "CustomTimePickerCtrl":
            value = self._editors[editorLabel][1]
            
            if value is None:
                value = itemText
            else:
                value = None   
            
            editor = _editor(self, value=value)
         
        font = self.GetFont()
        editor.SetFont(font)
            
        self.OpenEditor(selectedRow, selectedCol, editor)
        
    def __OnLeftDoubleClick(self, event):
        """ here we create and open an editor """
        selectedRow, selectedCol = self.GetSelectedItem()        
        columnList = [self.GetColumn(n).GetText() for n in range(self.GetColumnCount())]
        columnName = self.GetColumn(selectedCol).GetText()          
        itemText = self.GetItem(selectedRow, selectedCol).GetText()
        
        if itemText in self._editorIgnore:
            self.selectedRow = None
            self.selectedCol = None
            self.editorRow = None
            self.editorCol = None
            return
            
        """ no editors have been binded. Default behaviour is to match column name """        
        editorLabel = None
        if self._editorBind == {}:
            editorLabel = None            
        elif columnName not in [self._editorBind[bind]["col"] for bind in self._editorBind]:
            #if no bindings specify a condition for the columnName, 
            #we skip and just try to match the columnName with the
            #editorLabel
            editorLabel = columnName
        else:
            for e in self._editorBind:                
                col = self._editorBind[e]["col"]                
                if col != columnName:
                    continue
                ifcol = self._editorBind[e]["ifcol"]
                if ifcol is None:
                    editorLabel = e
                    break
                else:
                    #check all conditions are true                    
                    for matchCol, matchVal in ifcol.items():
                        findCol = columnList.index(matchCol)
                        findVal = self.GetItem(selectedRow, findCol).GetText()
                        if findVal == matchVal:
                            editorLabel = e
                            continue
                        else:
                            editorLabel = None
                            continue
                    
                    #we have a match, so use this editor
                    if editorLabel:
                        break
                    else:
                        continue
                        
        if editorLabel is None:
            editorLabel = columnName
        
        if editorLabel not in self._editors:
            #no editor. Do nothing
            print("no editor matched the context")
            self.selectedRow = None
            self.selectedCol = None
            self.editorRow = None
            self.editorCol = None
            return
        
        _editor = self._editors[editorLabel][0]
        editorType = _editor.GetEditorType()
        editorName = _editor.GetEditorName()
        
        if _editor.GetEditorType() == "control": 
            self._CreateControlEditor(editorLabel, editorName)
        elif _editor.GetEditorType() == "dialog": 
            self._CreateDialogEditor(editorLabel, editorName)
        else:
            raise Exception("invalid editor type")
            
    def OpenEditor(self, row, col, editor):
        """ Opens an editor at the current position """
        
        # destroy if another editor
        if hasattr(self, 'editor'):       
            self.editor.Destroy()            
        self.editor = editor
                
        x0 = self._selectedCol_len[col]
        x1 = self._selectedCol_len[col+1] - x0
        scrolloffset = self.GetScrollPos(wx.HORIZONTAL)
        # scroll forward
        if x0 + x1 - scrolloffset > self.GetSize()[0]:
            if wx.Platform == "__WXMSW__":
                # don't start scrolling unless we really need to
                offset = x0+x1-self.GetSize()[0] - scrolloffset
                # scroll a bit more than what is minimum required
                # so we don't have to scroll everytime the user presses TAB
                # which is very tireing to the eye
                addoffset = self.GetSize()[0]/4
                # but be careful at the end of the list
                if addoffset + scrolloffset < self.GetSize()[0]:
                    offset += addoffset

                self.ScrollList(offset, 0)
                scrolloffset = self.GetScrollPos(wx.HORIZONTAL)
            else:
                # Since we can not programmatically scroll the ListCtrl,
                # close the editor so the user can scroll and reopen the editor
                self.editor.SetValue(self.GetItem(row, col).GetText())
                self._selectedRow = row
                self._selectedColumn = col
                self.CloseEditor()
                return

        y0 = self.GetItemRect(row)[1]
        editor.SetSize(x0-scrolloffset, y0, x1, 19)        
        
        editor.Show()
        editor.Raise()        
        editor.SetFocus()
        editor = self.editor
        
        self._editorRow = row
        self._editorCol = col
            
            
    def CloseEditor(self, event=None):
        """ Close the editor and save the new value to the ListCtrl. """
        
        #single editor mode. opening a new editor closes the previous one
        if not hasattr(self, 'editor'):
            return
                
        try:
            newText = self.editor.ShowModal()            
        except:
            self.editor.Hide()
            newText = self.editor.GetValue()
                        
        self.SetFocus()

        # post wxevent_COMMAND_LIST_END_LABEL_EDIT
        # Event can be vetoed. It doesn't have SetEditCanceled(), what would
        # require passing extra argument to CloseEditor()
        event = wx.ListEvent(wx.wxEVT_COMMAND_LIST_END_LABEL_EDIT, self.GetId())
        item = self.GetItem(self._editorRow, self._editorCol)        
        event.Item.SetId(item.GetId())
        event.Item.SetColumn(item.GetColumn())
        event.Item.SetData(item.GetData())
        event.Item.SetText(str(newText)) #should be empty string if editor was canceled
        ret = self.GetEventHandler().ProcessEvent(event)
        if not ret or event.IsAllowed():
            if self.IsVirtual():
                # replace by whatever you use to populate the virtual ListCtrl
                # data source
                self.SetVirtualData(self._editorRow, self._editorCol, text)
            else:
                self.SetItem(self._editorRow, self._editorCol, str(newText))
        self.RefreshItem(self._editorRow)
        
        self.selectedRow = None
        self.selectedCol = None
        self.editorRow = None
        self.editorCol = None
        # self.Refresh()

    def OnCharEditor(self, event):
        ''' Catch event TAB, Shift-TAB, cursor DOWN/UP key code
        so we can open event editor at event next column (if any) '''  
        
        #navigating the list control only editor is closed
        if not self.editor.IsShown():
            return
            
        def _SelectIndex(self, row):
            listlen = self.GetItemCount()
            if row < 0 and not listlen:
                return
            if row > (listlen-1):
                row = listlen -1

            self.SetItemState(self._selectedRow, ~wx.LIST_STATE_SELECTED,
                              wx.LIST_STATE_SELECTED)
            self.EnsureVisible(row)
            self.SetItemState(row, wx.LIST_STATE_SELECTED,
                              wx.LIST_STATE_SELECTED)
                          
        keycode = event.GetKeyCode()        
        if keycode == wx.WXK_TAB:
            self.CloseEditor()
            if self._selectedColumn + 1 < self.GetColumnCount():
                self.OpenEditor(self._selectedColumn + 1, self._selectedRow)                
        elif keycode == wx.WXK_TAB and event.ShiftDown():
            self.CloseEditor()
            if self._selectedColumn - 1 >= 0:
                self.OpenEditor(self._selectedColumn - 1, self._selectedRow)
        elif keycode == wx.WXK_DOWN:
            self.CloseEditor()
            if self._selectedRow + 1 < self.GetItemCount():
                SelectIndex(self._selectedRow + 1)
                self.OpenEditor(self._selectedColumn, self._selectedRow)
        elif keycode == wx.WXK_UP:
            self.CloseEditor()
            if self._selectedRow > 0:
                SelectIndex(self._selectedRow - 1)
                self.OpenEditor(self._selectedColumn, self._selectedRow)        
        elif keycode == wx.WXK_ESCAPE:
            self.CloseEditor()             
        else:
            return
            event.Skip()
            

            