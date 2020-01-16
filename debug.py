#!usr/bin/env python3
from code import *
from debug_statements import *

import os
import sys
from inspect import *
from collections import defaultdict

class debugger:
    def __init__(self, test_function):
        self.vars = defaultdict()
        # self.number = 0
        self.curr_line = None
        print("----------------Running Debug----------------")
        sys.settrace(self.trace_calls)
        test_function()


    def trace_calls(self, frame, event, arg):
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
                    on_var_change(self.curr_line, varname, self.vars[varname], varvalue)
            else:
                on_var_init(self.curr_line, varname, varvalue)
            self.vars[varname] = frame.f_locals[varname]
        self.curr_line = frame.f_lineno

debugger(testfunc)