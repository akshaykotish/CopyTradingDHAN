from Controller.Control import Control

import os
import sys
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

if not is_admin():
    print("Re-running script as an administrator...")
    run_as_admin()
    sys.exit()
else: 
    control = Control()
    control.Execute()

