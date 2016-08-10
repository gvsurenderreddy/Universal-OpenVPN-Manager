"""
<Universal OpenVPN Manager - A GUI front-end for OpenVPN>
Copyright (C) 2016, Simon Wu, <swprojects@gmx.com>
 
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Softwares
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import sys
import os
import traceback
import win32api, win32con, win32event, win32process
from win32process import CreateProcess
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon
from multiprocessing import Process, Queue

def IsUserAdmin():
    """ Checks if the user has admin/root privileges """
    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print("Admin check failed, assuming not an admin.")
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        raise(RuntimeError, "Unsupported operating system for this module: %s" % (os.name,))

def RunAsAdmin(conn=None, cmdLine=None, showCmd=False, wait=True):
    
        
    if os.name != 'nt':
        raise(RuntimeError, "This function is only implemented on Windows.")
    
    if cmdLine is None:
        python_exe = sys.executable    
        cmdLine = [python_exe] + sys.argv        
    else: 
        try:
            #check if list/tuple
            ",".join(cmdLine)
            print(cmdLine[0])
        except:
            raise Exception(TypeError, cmdLine, "cmdLine is not a list or a tuple type")
    
    cmd = cmdLine[0]              
    params = " ".join([x for x in cmdLine[1:]])
       
    #show shell or keep it hidden    
    if showCmd is True:        
        showCmd = win32con.SW_SHOWNORMAL
    elif showCmd is False:    
        showCmd = win32con.SW_HIDE
    else:  
        raise Exception(ArgError, "showCmd: Invalid value - ", showCmd)
        
    lpVerb = 'runas'  # causes UAC elevation prompt.
    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)
                              
    # cmd+= " " +params
    # procHandle, threadHandle, procId, threadId = DoCreateProcess(cmd) 
    if conn:
        pass
        conn.put("")
        
    if wait:
        procHandle = procInfo['hProcess']   
        # print        ("pr",prponerocHandle
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        print ("Process handle %s returned code %s" % (procHandle, rc))
    else:
        rc = None
    return rc
    
    
    
def Test():
    rc = 0
    if not IsUserAdmin():
        # print("You're not an admin.", os.getpid(), "params: ", sys.argv)
        # rc = run_as_admin(["c:\\Windows\\notepad.exe"])
        rc = RunAsAdmin("s")
    else:
        print("You are an admin!", os.getpid(), "params: ", sys.argv)
        rc = 0
    x = input('Press Enter to exit.')
    return rc


if __name__ == "__main__":
    sys.exit(Test())