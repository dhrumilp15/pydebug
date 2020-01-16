#!usr/bin/env python3
import os
from inspect import *

def on_var_change(lineno : int, varname : str, old, new):
    print(f"On line {lineno}: {varname} changes from {old} to {new}")

def on_var_init(lineno : int, varname : str, varvalue : str):
    print(f"On line {lineno}: {varname} is initialized to {varvalue}")

def call_print(frame):
    frameinfo = getframeinfo(frame)
    print(f'''
    File: {os.path.basename(frameinfo.filename)}
    Function: {frameinfo.function} on Line: {frameinfo.lineno}
    ''')