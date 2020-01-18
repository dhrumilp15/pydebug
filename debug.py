#!usr/bin/env python3
from code import *
from debug_statements import *
# from record import record

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
        self.lineno = None
        self.function_name = test_function.__name__

        self.record = defaultdict(list)
        
        self.outfile = "report.log"
        self.main(test_function)
    
    def main(self, test_function: FunctionType):
        open(self.outfile, "w").close()
        print("----------------Running Debug----------------")
        sys.settrace(self.trace_calls)
        test_function()

        self.closing()
        self.print_record()


    def trace_calls(self, frame, event, arg):
        if getframeinfo(frame).function == self.function_name:
            call_print(frame)
            self.lineno = frame.f_lineno
            for varname in frame.f_code.co_varnames:
                self.vars[varname] = None
            return self.trace_lines

    def trace_lines(self, frame, event, arg):
        # self.number += 1
        for varname, varvalue in frame.f_locals.items():
            if self.vars[varname]:
                if not self.vars[varname] == varvalue:
                    self.on_var_change(varname, self.vars[varname], varvalue)
                    self.write_to_file(varname, self.vars[varname], varvalue)
                    self.record[varname].append((getframeinfo(frame).function, self.lineno, varvalue))
            else:
                self.write_to_file(varname, varvalue)
                print_var_init(self.lineno, varname, varvalue)
                self.record[varname].append((getframeinfo(frame).function, self.lineno, varvalue))
            self.vars[varname] = frame.f_locals[varname]
        self.lineno = frame.f_lineno
    
    def on_var_change(self, varname : str, old, new):
        CollectionTypes = list, dict, set, tuple
        
        if isinstance(old, CollectionTypes) and isinstance(new, CollectionTypes):
            
            if isinstance(old, dict) and isinstance(new, dict):                
                removed = dict(set(old.items()) - set(new.items())) # Strictly which KEYS have been removed
                added = dict(set(new.items()) - set(old.items())) # Strictly which KEYS have been added
                print(added)
                gcddict = set(old) & set(new) # Common keys may not have the same values
                changekeys = {}
                for key in gcddict:
                    if not old[key] == new[key]:
                        changekeys.update({key : new[key]})
                if changekeys:
                    print_var_change(self.lineno, varname, removed, added, changekeys)
                else:
                    print_var_change(self.lineno, varname, removed, added)
            else:
                oldchanges = list(set(old) - set(new)) # What is in old but not in new, these are what has been removed
                newchanges = list(set(new) - set(old)) # What is in new but not in old
                print_var_change(self.lineno, varname, oldchanges, newchanges)
        else:
            print_var_change(self.lineno, varname, old, new)
    
    def write_to_file(self, varname : str, old, new = None):
        with open(self.outfile, "a") as f:
            if new:
                f.write(f"{self.lineno} - {varname} : {old} -> {new}\n")
            else:
                f.write(f"{self.lineno} - {varname} : {old}\n")
    
    def closing(self):
        print("\n----------------Finished Debug----------------")
        print("See the execution history and the report in the report.log!")
    
    def print_record(self):
        with open(self.outfile, "a") as f:
            for varname, info in self.record.items():
                f.write(f"\nFor the variable \'{varname}\'\n")
                init = info[0]

                initialType = type(init[2])
                f.write(f"\tType: {initialType.__name__}\n")
                f.write(f"\tInstantiated in function \'{init[0]}\' on line {init[1]}\n")
                values = []
                
                if initialType is Sequence:
                    f.write("\tValues:\n")
                for detail in info:
                    # print(initialType)
                    if not type(detail[2]) == initialType:
                        f.write(f"\tOn line {detail[1]} in function \'{detail[0]}\': Change in type from {initialType.__name__} to {type(detail[2]).__name__}\n")
                        f.write(f"\n\tCurrent Type: {type(detail[2]).__name__}\n")
                        values.clear()
                    initialType = type(detail[2])
                    values.append(detail[2])
                    if initialType is str:
                        f.write(f"\t - On line {detail[1]} in function \'{detail[0]}\', {detail[2]}\n")
                if initialType is int:
                    f.write(f"\t - Min: {min(values)}, Max: {max(values)}\n")

# If this file is called directly from the commandline
if __name__ == "__main__":
    argc = len(sys.argv)
    if argc > 1:
        if "--help" in sys.argv or "-h" in sys.argv:
            helper()
    else:
        debugger(testfunc)