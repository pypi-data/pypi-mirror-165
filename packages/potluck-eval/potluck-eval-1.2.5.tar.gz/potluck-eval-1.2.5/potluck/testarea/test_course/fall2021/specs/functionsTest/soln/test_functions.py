"""
Authors: Peter Mawhorter
Consulted:
Date: 2022-1-23
Purpose: Tests for basic functions using optimism
"""

import math

import functions

import optimism as opt

# indentMessage tests
m = opt.testFunction(functions.indentMessage)
m.case('hi', 4).checkReturnValue('  hi')
m.case('hello', 4).checkReturnValue('hello')


# printMessage tests
m = opt.testFunction(functions.printMessage)
m.case('hi', 4).checkPrintedLines('  hi')
m.case('hello', 4).checkPrintedLines('hello')


# ellipseArea tests
m = opt.testFunction(functions.ellipseArea)
m.case(1, 1).checkReturnValue(math.pi)
m.case(2, 3).checkReturnValue(6 * math.pi)


# No way to define test cases for polygon...
