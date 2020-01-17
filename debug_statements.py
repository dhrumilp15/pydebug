#!usr/bin/env python3
import os
from inspect import *

def on_var_change(lineno : int, varname : str, outfile : str, old, new):
    print(f"On line {lineno}: {varname} changes from {old} to {new}")
    # For easier testing
    with open(outfile, "a") as f:
        f.write(f"{lineno} - {varname} : {old} -> {new}\n")

def on_var_init(lineno : int, varname : str, outfile : str, varvalue : str):
    print(f"On line {lineno}: {varname} is initialized to {varvalue}")
    # For easier testing
    with open(outfile, "a") as f:
        f.write(f"{lineno} - {varname} : {varvalue}\n")

def call_print(frame):
    frameinfo = getframeinfo(frame)
    print(f'''
        File: {os.path.basename(frameinfo.filename)}
        Function: {frameinfo.function}
        Defined on Line: {frameinfo.lineno}
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