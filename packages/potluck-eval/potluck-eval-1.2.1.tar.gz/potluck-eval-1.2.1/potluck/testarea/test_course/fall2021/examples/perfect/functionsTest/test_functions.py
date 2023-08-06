"""
Authors: Peter Mawhorter
Consulted:
Date: 2022-1-23
Purpose: Tests for basic functions using optimism (alternate)
"""

import math

import functions

import optimism as opt

# indentMessage tests
m = opt.testFunction(functions.indentMessage)
m.case('hello', 8).checkReturnValue('   hello')
m.case('hi', 1).checkReturnValue('hi')
m.case('hi', 3).checkReturnValue(' hi')


# printMessage tests
m = opt.testFunction(functions.printMessage)
m.case('hello', 8).checkPrintedLines('   hello')
m.case('hi', 1).checkPrintedLines('hi')
m.case('has\nnewline', 3).checkPrintedLines('has', 'newline')
m.case('has\nnewline', 14).checkPrintedLines('   has', 'newline')


# ellipseArea tests
m = opt.testFunction(functions.ellipseArea)
m.case(1, 1).checkReturnValue(math.pi)
m.case(3, 2).checkReturnValue(6 * math.pi)
m.case(0.4, 0.5).checkReturnValue(0.2 * math.pi)


# No way to define test cases for polygon...
