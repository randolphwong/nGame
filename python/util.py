import re

def prefixCalculator(expr):
    stack = []
    split_expr = re.findall(r'\+|\-|\*|\/|\d+(?:\.\d*)?', expr)[::-1]
    for i in split_expr:
        if not i in '+-*/':
            stack.append(str(float(i)))
        else:
            operand1 = stack.pop(-1)
            operand2 = stack.pop(-1)
            result = eval(operand1 + i + operand2)
            stack.append(str(result))
    return float(stack[0])

def prefixToInfix(expr):
    stack = []
    split_expr = re.findall(r'\+|\-|\*|\/|\d+(?:\.\d*)?', expr)[::-1]
    for i in split_expr:
        if not i in '+-*/':
            stack.append(i)
        else:
            operand1 = stack.pop(-1)
            operand2 = stack.pop(-1)
            result = '({} {} {})'.format(operand1, i, operand2)
            stack.append(result)
    return stack[0][1:-1]

'''
import time
from expressionTree import *

def stress():
    c = time.time()
    for i in xrange(1000000):
        #a = parse('5 25 75 / 100 + 10 4 - * +')
        #a = PrefixCalculator('+ * + / 25 75 100 - 10 4 5')
        a = ExprTree('+', 5, ExprTree('*', ExprTree('+', ExprTree('/', 25, 75), 100), ExprTree('-', 10, 4))).evaluate()
    print time.time() - c, 'secs'

'''
