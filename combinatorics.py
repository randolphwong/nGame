from util import *
from expressionTree import *
import itertools as IT
import time
import random
import os
import math

class Combinatorics:
    operator = '*/+-'
    expr_file = None
    def __init__(self, n):
        self.setNewNumbers(n)

    def setNewNumbers(self, n):
        self.n = n

    def remainsFromSeqSubtract(self, target, src):
        new_list = target[:]
        for n in src:
            new_list.remove(n)
        return new_list

    def allPartition(self, set_sequence):
        for i in xrange(1, len(set_sequence)):
            for c in IT.combinations(set_sequence, i):
                yield (list(c), self.remainsFromSeqSubtract(set_sequence, c))

    def findAllPossibleExprTree(self, num_list):
        num_list_length = len(num_list)
        if num_list_length == 1:
            for number in num_list:
                yield number
        else:
            part1_old = None
            for part1, part2 in self.allPartition(num_list):
                if part2 == part1_old: break
                part1_old = part1
                for op in '*/+-':
                    for expr1 in self.findAllPossibleExprTree(part1):
                        for expr2 in self.findAllPossibleExprTree(part2):
                            yield ExprTree(op, expr1, expr2)
                            yield ExprTree(op, expr2, expr1)


    def findNonRedundantExprTree(self, num_list):
        num_list_length = len(num_list)
        if num_list_length == 1:
            for number in num_list:
                yield number
        else:
            part1_old = None
            for part1, part2 in self.allPartition(num_list):
                if part2 == part1_old: break
                part1_old = part1
                for op in '*/+-':
                    for expr1 in self.findNonRedundantExprTree(part1):
                        for expr2 in self.findNonRedundantExprTree(part2):
                            yield ExprTree(op, expr1, expr2)
                            if (op == '/' or op == '-') and \
                               part1 != part2:
                                yield ExprTree(op, expr2, expr1)

    def writeAllExpr(self, exprs, max_write_size):
        line_byte = None
        counter = 0
        with open('all expr.txt', 'w') as f:
            for e in exprs:
                if max_write_size is not None:
                    if line_byte is None:
                        line_byte = len(e.toPrefix()) + 1
                    if counter >= max_write_size:
                        break
                    counter += line_byte
                f.write(e.toPrefix() + '\n')

    def getRandomExpr(self, exprs, max_write_size):
        if self.expr_file is None:
            file_name = self.writeAllExpr(exprs, max_write_size)
            self.expr_file = open('all expr.txt', 'r')
            self.expr_file.seek(0, os.SEEK_END)
            total_byte = self.expr_file.tell()
            self.expr_file.seek(0)
            self.expr_file.readline()
            self.new_line_byte = int(self.expr_file.tell())
            self.last_line = int(total_byte/self.new_line_byte) - 1
        while True:
            random_line = random.randint(0, self.last_line)
            self.expr_file.seek(random_line*self.new_line_byte)
            yield self.expr_file.read(self.new_line_byte - 2)

    def getValidExpression(self, result, up_to=None, randomise=False, max_write_size=None):
        complete_expr = self.findNonRedundantExprTree(self.n)
        if randomise == True:
            complete_expr = self.getRandomExpr(complete_expr, max_write_size)
            return self.getRandomisedExpression(result, complete_expr, up_to=up_to)
        valid_expr = []
        self.total_combinations = 0
        for expr in complete_expr:
            self.total_combinations += 1
            try:
                calculated = expr.evaluate()
                if abs(calculated - result) < 0.001:
                    valid_expr.append(str(expr)[1:-1])
            except:
                pass
            if up_to is not None:
                if len(valid_expr) >= up_to:
                    break
        return valid_expr

    def getRandomisedExpression(self, result, complete_expr, up_to=None):
        valid_expr = []
        self.total_combinations = 0
        for expr in complete_expr:
            self.total_combinations += 1
            try:
                if abs(prefixCalculator(expr) - result) < 0.001:
                    valid_expr.append(prefixToInfix(expr))
            except:
                pass
            if up_to is not None:
                if len(valid_expr) >= up_to:
                    break
        return valid_expr
        

    def evaluate(self, result, up_to=None, randomise=False, max_write_size=None):
        start_time = time.time()
        valid_expr = self.getValidExpression(result, up_to=up_to,
                                             randomise=randomise,
                                             max_write_size=max_write_size)
        t = round(time.time() - start_time, 2)
        solution_msg = '{} solutions found after comparing with {} enumerated combinations.\n'
        solution_msg = solution_msg.format(len(valid_expr), self.total_combinations)
        time_taken_msg = 'Time taken for computation: {}s\n'.format(t)
        text = 'Number list: {}\nTarget number: {}\n'.format(self.n, result) \
               + solution_msg + time_taken_msg
        if len(valid_expr) != 0:
            text += 'First 10 solutions:\n'
            if len(valid_expr) > 10:
                random_ten = sorted(random.sample(valid_expr, 10))
            else:
                random_ten = valid_expr
            text += '\n'.join(random_ten)
        if self.expr_file is not None:
            self.expr_file.close()
            self.expr_file = None
        return text
