#!usr/bin/env python3
from code import *
from debug_statements import *

import os
import sys
from inspect import *
from collections import defaultdict
from types import *
from collections.abc import *

class debugger:
    """
    Main Debugger Class, drives debugging and traces calls and lines
    """
    def __init__(self, test_function: FunctionType):
        """
        Debugger constructor
        :param test_function: FunctionType, This is the function to debug
        """
        # self.number = 0
        
        self.vars = defaultdict()
        self.curr_line = None
        self.function_name = test_function.__name__
        
        self.outfile = "output.log"
        open(self.outfile, "w").close()
        
        print("----------------Running Debug----------------")
        sys.settrace(self.trace_calls)
        test_function()

        self.closing()


    def trace_calls(self, frame, event, arg):
        if getframeinfo(frame).function == self.function_name:
            call_print(frame)
            self.line = frame.f_lineno
            for varname in frame.f_code.co_varnames:
                self.vars[varname] = None
            return self.trace_lines

    def trace_lines(self, frame, event, arg):
        # self.number += 1
        for varname, varvalue in frame.f_locals.items():
            if self.vars[varname]:
                if not self.vars[varname] == varvalue:
                    self.on_var_change(self.curr_line, varname, self.outfile, self.vars[varname], varvalue)
            else:
                self.on_var_init(self.curr_line, varname, self.outfile, varvalue)
            self.vars[varname] = frame.f_locals[varname]
        self.curr_line = frame.f_lineno
    
    def on_var_change(self, lineno : int, varname : str, outfile : str, old, new):
        CollectionTypes = list, dict, set, tuple
        with open(outfile, "a") as f:
            f.write(f"{lineno} - {varname} : {old} -> {new}\n")
        
        if isinstance(old, CollectionTypes) and isinstance(new, CollectionTypes):
            # Handle removed, added, changed
            oldchanges = list(set(old) - set(new)) # What is in old but not in new, these are what has been removed
            newchanges = list(set(new) - set(old)) # What is in new but not in old
            # print("Old, new:", old, new)
            # print("oldchanges, newchanges: ", oldchanges,newchanges)
            print_var_change(lineno, varname, outfile, oldchanges, newchanges)
        else:
            print_var_change(lineno, varname, outfile, old, new)

    def on_var_init(self, lineno : int, varname : str, outfile : str, varvalue : str):
        with open(outfile, "a") as f:
            f.write(f"{lineno} - {varname} : {varvalue}\n")
        print_var_init(lineno, varname, outfile, varvalue)
    
    def closing(self):
        print("\n----------------Finished Debug----------------")
        print("See your results in output.log!")
    

# If this file is called directly from the commandline
if __name__ == "__main__":
    argc = len(sys.argv)
    if argc > 1:
        if "--help" in sys.argv or "-h" in sys.argv:
            helper()
    else:
        debugger(testfunc)