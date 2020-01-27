# !usr/bin/env python3
from code import *
from debug_statements import *
from jsonhandler import *

import os
import sys
from inspect import *
from collections import defaultdict
from types import *
from collections.abc import *
from time import time
import importlib.util
import argparse

class Debugger:
    """
    Main Debugger Class, sets up for either reporting or analyzing
    """
    
    def __init__(self, test_function: FunctionType = None, json_report = None):
        """
        Debugger constructor
        :param test_function: FunctionType, This is the function to debug
        """
        # self.number = 0
        self.start_time = time()
        self.vars = defaultdict()
        self.line_times = []
        self.json_report = json_report

        if json_report:
            self.record = load_json(json_report)
            self.print_record()
        else:

            self.lineno = None
            self.function_name = test_function.__name__
            self.startline = 0
            
            self.step = 0

            self.record = defaultdict(list)
            
            self.outfile = "report.json"
            self.main(test_function)


    def main(self, test_function: FunctionType):
        """
        Main Debugger Activity, drives debugging and traces calls and lines
        """

        open(self.outfile, "w").close() # Empty the report
        
        print("----------------Running Debug----------------")
        sys.settrace(self.trace_calls)
        test_function()

        self.closing()
        save_json_report(self.record, self.outfile)

    def trace_calls(self, frame, event, arg):
        frameinfo = getframeinfo(frame)
        if frameinfo.function == self.function_name:
            self.record["header"] = {
                "File" : os.path.basename(frameinfo.filename),
                "Function" : frameinfo.function,
                "Initial Line" : frame.f_lineno,
                "start_time" : self.start_time
            }
            self.record["body"] = defaultdict(list)
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
            flag = True
            if self.vars[varName]:
                if not self.vars[varName] == varvalue:
                    self.on_var_change(varName, self.vars[varName], varvalue)
                else:
                    flag = False
            else:
                print_var_init(varName, varvalue)
                
            if flag:
                self.record["body"][self.step].append({
                        "name" : varName,
                        "timestamp" : time(),
                        "function" : getframeinfo(frame).function,
                        "lineno" : self.lineno,
                        "value" : varvalue
                        })
            self.vars[varName] = frame.f_locals[varName]
        self.lineno = frame.f_lineno
        self.line_times.append(time() - start_of_line)
        if not start:
            print("\tProcessing this line took: {:.4f} seconds".format(time() - start_of_line))
            print("\tExecution to this line has taken: {:.4f} seconds".format(time() - self.start_time))
        self.step += 1 # Increment step
    
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
    

    def print_record(self):
        print(f"------------Reading From {self.json_report}------------")
        print(f"""
        File: {self.record["header"]["File"]}
        Function : {self.record["header"]["Function"]}
        Starts on Line : {self.record["header"]["Initial Line"]}
        """)
        initialTime = self.record["header"]["start_time"]
        for step, info in self.record["body"].items():
            print("On line {}:".format(
                info[0]["lineno"]
            ))
            for change in info:
                if change["name"] in self.vars:
                    print("\t\'{}\' changes from {} to {}".format(
                        change["name"], self.vars[change["name"]], change["value"]
                    ))
                else:
                    print("\t\'{}\' is initialized to {}".format(
                        change["name"], change["value"]
                    ))
                    self.vars[change["name"]] = change["value"]
            if step != "1":
                # print(self.record["body"][str(int(step) - 1)])
                self.line_times.append(change["timestamp"] - self.record["body"][str(int(step) - 1)][0]["timestamp"])
                print("\tProcessing this line took {:.4f} seconds".format(change["timestamp"] - self.record["body"][str(int(step) - 1)][0]["timestamp"]))
            print("\tExecution to this line took {:.4f} seconds".format(change["timestamp"] - initialTime))
        print("\nProcessing each line took an average of {:.4f} seconds".format(sum(self.line_times) / len(self.line_times)))

# If this file is called directly from the commandline
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("py_file", nargs='?', type=str, help="python file to debug", default=None)
    parser.add_argument("function", nargs='?', type=str, help="function to debug", default=None)
    parser.add_argument("json_file", nargs='?', type=str, help="report save location", default="report.json")
    args = parser.parse_args()
    if args.py_file:
        spec = importlib.util.spec_from_file_location("pydebug", args.py_file) # Assume in the same python package
        test = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test)
        found = False
        if args.function:
            if hasattr(test, args.function):
                Debugger(getattr(test, args.function))
                found = True
        else:
            if hasattr(test, "main"):
                Debugger(test.main)
                found = True
        if not found:
            Debugger(getattr(test, "test"))
    else:
        Debugger(main)