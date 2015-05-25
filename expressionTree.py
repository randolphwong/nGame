class ExprTree:
    def __init__(self, operator, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2
        self.operator = operator

    def hasOnlyMultiplication(self):
        return (self.operand1.hasOnlyMultiplication() \
                if isinstance(self.operand1, ExprTree) else True) and \
                (self.operand2.hasOnlyMultiplication() \
                if isinstance(self.operand2, ExprTree) else True) and \
                self.operator == '*'

    def hasOnlyAddition(self):
        return (self.operand1.hasOnlyAddition() \
                if isinstance(self.operand1, ExprTree) else True) and \
                (self.operand2.hasOnlyAddition() \
                if isinstance(self.operand2, ExprTree) else True) and \
                self.operator == '+'

    def hasOnlyPlusMinus(self):
        return (self.operand1.hasOnlyPlusMinus() \
                if isinstance(self.operand1, ExprTree) else True) and \
                (self.operand2.hasOnlyPlusMinus() \
                if isinstance(self.operand2, ExprTree) else True) and \
                (self.operator == '+' or self.operator == '-')

    def evaluate(self):
        if isinstance(self.operand1, ExprTree):
            operand1_value = self.operand1.evaluate()
        else:
            operand1_value = self.operand1
        if isinstance(self.operand2, ExprTree):
            operand2_value = self.operand2.evaluate()
        else:
            operand2_value = self.operand2
            
        if self.operator == '*':
            return operand1_value * operand2_value
        elif self.operator == '+':
            return operand1_value + operand2_value
        elif self.operator == '-':
            return operand1_value - operand2_value
        elif self.operator == '/':
            return operand1_value / float(operand2_value)
        else:
            return 'eval error'

    def toPrefix(self):
        if isinstance(self.operand1, ExprTree):
            opn1 = self.operand1.toPrefix()
        else:
            opn1 = self.operand1
        if isinstance(self.operand2, ExprTree):
            opn2 = self.operand2.toPrefix()
        else:
            opn2 = self.operand2
        return '{} {} {}'.format(self.operator,
                                 opn1,
                                 opn2)

##    def __str__(self):
##        return '{} {} {}'.format(self.operator, self.operand1,
##                                 self.operand2)
    def __str__(self):
        '''Returns in infix notation'''
        return '({} {} {})'.format(self.operand1, self.operator,
                                 self.operand2)

    def __eq__(self, expr):
        if isinstance(expr, ExprTree):
            expr = expr.evaluate()
        return self.evaluate() == expr

    def __ne__(self, expr):
        if isinstance(expr, ExprTree):
            expr = expr.evaluate()
        return self.evaluate() != expr
