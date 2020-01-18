#!usr/bin/env python3
import os
from inspect import *

def print_var_change(lineno : int, varname : str, old : list, new : list, changekeys : dict = None):    
    changetypes = list, dict

    if isinstance(old, changetypes) and isinstance(new, changetypes):
        print(f"On line {lineno}:")
        if old and new: # If there are objects in old that aren't in new and there are objects in new that aren't in old
            if isinstance(old,dict) and isinstance(new,dict):
                for key in changekeys:
                    print(f"\tThe value at \'{key}\' changes from {old[key]} to {new[key]} in \'{varname}\'")

                print(f"\t{old} is removed from \'{varname}\'")
                print(f"\t{new} is added to \'{varname}\'")
            else:
                print(f"\t{old} is removed from \'{varname}\'")
                print(f"\t{new} is added to \'{varname}\'")
        elif old:
            print(f"\t{old} is removed from \'{varname}\'")
        elif new:
            print(f"\t{new} is added to \'{varname}\'")
    else:
        print(f"On line {lineno}: \'{varname}\' changes from {old} to {new}")
    
def print_var_init(lineno : int, varname : str, varvalue : str):
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

        This also writes a sparser representation of the debug to output.log for persistent storage!
        -----------------------------------------
    ''')