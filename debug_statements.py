#!usr/bin/env python3
import os
from inspect import *

def print_var_change(lineno : int, varname : str, outfile : str, old, new):    
    # print("A CALL")
    if isinstance(old, list) and isinstance(new, list):
        print(f"On line {lineno}:")
        if old and new: # If there are objects in old that aren't in new and there are objects in new that aren't in old
            print(f"\t{old} are removed from \'{varname}\'")
            print(f"\t{new} are added to \'{varname}\'")
        elif old and not new:
            print(f"\t{old} are removed from \'{varname}\'")
        elif new and not old:
            print(f"\t{new} are added to \'{varname}\'")
    else:
        print(f"On line {lineno}: \'{varname}\' changes from {old} to {new}")
    
def print_var_init(lineno : int, varname : str, outfile : str, varvalue : str):
    print(f"On line {lineno}: \'{varname}\' is initialized to {varvalue}")
    
def call_print(frame):
    frameinfo = getframeinfo(frame)
    print(f'''
        File: {os.path.basename(frameinfo.filename)}
        Function: {frameinfo.function}
        Starts on Line: {frameinfo.lineno}
    ''')

def helper():
    print('''
        -----------------------------------------
        Welcome to Dhrumil's Epic Python Debugger!

        Please add your code to the "code.py" file for testing!

        Usage: python debug.py

        This also writes a sparser representation of the debug to output.log for persistent storage
        -----------------------------------------
    ''')