#!usr/bin/env python3
from code import *
from debug_statements import *

import os
import sys
from inspect import *
from collections import defaultdict
from types import *
from collections.abc import *
from time import time


class Debugger:
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
        self.empty = True

        self.lineno = None
        self.function_name = test_function.__name__
        self.startline = 0
        
        self.start_time = time()
        self.line_times = []

        self.record = defaultdict(list)
        
        self.outfile = "report.log"
        self.main(test_function)

    def main(self, test_function: FunctionType):
        open(self.outfile, "w").close()
        print("----------------Running Debug----------------")
        sys.settrace(self.trace_calls)
        test_function()

        self.closing()
        self.write_record()

    def trace_calls(self, frame, event, arg):
        if getframeinfo(frame).function == self.function_name:
            call_print(frame)
            self.lineno = frame.f_lineno
            self.startline = frame.f_lineno
            for varName in frame.f_code.co_varnames:
                self.vars[varName] = None
            return self.trace_lines

    def trace_lines(self, frame, event, arg):
        # self.number += 1
        start = self.lineno == self.startline 
        if not start:
            print(f"On line {self.lineno}:")
        # print(getframeinfo(frame))
        start_of_line = time()
        for varName, varvalue in frame.f_locals.items():
            if self.vars[varName]:
                if not self.vars[varName] == varvalue:
                    self.on_var_change(varName, self.vars[varName], varvalue)
                    self.record[varName].append((getframeinfo(frame).function, self.lineno, varvalue))
            else:
                print_var_init( varName, varvalue)
                self.record[varName].append((getframeinfo(frame).function, self.lineno, varvalue))
            self.vars[varName] = frame.f_locals[varName]
        self.lineno = frame.f_lineno
        self.line_times.append(time() - start_of_line)
        if not start:
            print("\tProcessing this line took: {:.4f} seconds".format(time() - start_of_line))
            print("\tExecution to this line has taken: {:.4f} seconds".format(time() - self.start_time))
    
    def on_var_change(self, varName : str, old, new):
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
                    print_var_change( varName, removed, added, changekeys)
                else:
                    print_var_change( varName, removed, added)
            else:
                oldchanges = list(set(old) - set(new)) # What is in old but not in new, these are what has been removed
                newchanges = list(set(new) - set(old)) # What is in new but not in old
                print_var_change(varName, oldchanges, newchanges)
        else:
            print_var_change(varName, old, new)
    
    def write_to_file(self, log : str, heading : bool = False):
        with open(self.outfile, "a") as f:
            if heading:
                if f.tell() != 0:
                    f.write("\n")
                f.write(f"{log}\n")
            else:
                f.write(f"\t{log}\n")

    
    def closing(self):
        print("\nProcessing each line took an average of {:.4f} seconds".format(sum(self.line_times) / len(self.line_times)))
        print("\n----------------Finished Debug----------------")
        print("See the execution history and the report in the report.log!")

    def write_record(self):
        for varName, info in self.record.items():
            self.write_to_file(f"For the variable \'{varName}\'", heading=True)
            init = info[0]

            initialtype = type(init[2])
            self.write_to_file(f"Type: {initialtype.__name__}")
            self.write_to_file(f"Instantiated in function \'{init[0]}\' on line {init[1]}")
            values = []

            if isinstance(init[2], Collection):
                self.write_to_file("Values:")
            for detail in info:
                # print(initialtype)
                if not type(detail[2]) == initialtype:
                    self.write_to_file(f" - Initial Value: {values[0]}, Final Value: {values[-1]}\n")
                    self.write_to_file(f"On line {detail[1]} in function \'{detail[0]}\': Change in type from {initialtype.__name__} to {type(detail[2]).__name__}")
                    self.write_to_file(f"\tCurrent Type: {type(detail[2]).__name__}")
                    values.clear()
                initialtype = type(detail[2])
                values.append(detail[2])
                if initialtype is str:
                    self.write_to_file(f" - On line {detail[1]} in function \'{detail[0]}\', {detail[2]}")
            if initialtype is int:
                self.write_to_file(f" - Min: {min(values)}, Max: {max(values)}")
            self.write_to_file(f" - Initial Value: {values[0]}, Final Value: {values[-1]}")
        self.write_to_file("Total Execution Time: {:.4f} seconds".format(time() - self.start_time))


# If this file is called directly from the commandline
if __name__ == "__main__":
    argc = len(sys.argv)
    if argc > 1:
        if "--help" in sys.argv or "-h" in sys.argv:
            helper()
    else:
        Debugger(testfunc)
