#include "ExprTree.h"

std::string toString(double x) {
    std::ostringstream ss;
    ss << x;
    return ss.str();
}

ExprTree::ExprTree(double operand) {
    type = 1;
    operand1 = operand;
    exprStr = toString(operand);
}

ExprTree::ExprTree(const ExprTree& expr) {
    type = 2;
    operand1 = expr.eval();
    exprStr = expr.str();
}

ExprTree::ExprTree(char op, double operand1, double operand2) {
    type = 3;
    this->op = op;
    this->operand1 = operand1;
    this->operand2 = operand2;

    std::ostringstream ss;
    std::string op1, op2;
    op1 = toString(operand1);
    op2 = toString(operand2);
    ss << "(" << op1 << " " << op << " " << op2 << ")";
    exprStr = ss.str();
}

ExprTree::ExprTree(char op, ExprTree expr1, double operand2) {
    type = 4;
    this->op = op;
    this->operand1 = expr1.eval();
    this->operand2 = operand2;

    std::ostringstream ss;
    std::string op1, op2;
    op1 = expr1.str();
    op2 = toString(operand2);
    ss << "(" << op1 << " " << op << " " << op2 << ")";
    exprStr = ss.str();
}

ExprTree::ExprTree(char op, double operand1, ExprTree expr2) {
    type = 5;
    this->op = op;
    this->operand1 = operand1;
    this->operand2 = expr2.eval();

    std::ostringstream ss;
    std::string op1, op2;
    op1 = toString(operand1);
    op2 = expr2.str();
    ss << "(" << op1 << " " << op << " " << op2 << ")";
    exprStr = ss.str();
}

ExprTree::ExprTree(char op, ExprTree expr1, ExprTree expr2) {
    type = 6;
    this->op = op;
    this->operand1 = expr1.eval();
    this->operand2 = expr2.eval();

    std::ostringstream ss;
    std::string op1, op2;
    op1 = expr1.str();
    op2 = expr2.str();
    ss << "(" << op1 << " " << op << " " << op2 << ")";
    exprStr = ss.str();
}

double ExprTree::eval() const {
    if (type <= 2) // single operand
        return operand1;

    double result = 0;

    switch (op) {
        case '*':
            result = operand1 * operand2;
            break;
        case '/':
            result = operand1 / operand2;
            break;
        case '+':
            result = operand1 + operand2;
            break;
        case '-':
            result = operand1 - operand2;
            break;
    }
    return result;
}

std::string ExprTree::str() const {
    return exprStr;
}
