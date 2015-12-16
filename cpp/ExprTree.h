#ifndef EXPRTREE_H
#define EXPRTREE_H

#include <sstream>
#include <string>

class ExprTree {

public:
    ExprTree(){};
    ExprTree(double);
    ExprTree(const ExprTree&);
    ExprTree(char, double, double);
    ExprTree(char, ExprTree, double);
    ExprTree(char, double, ExprTree);
    ExprTree(char, ExprTree, ExprTree);

    double eval() const;
    std::string str() const;

private:
    char type;
    char op;
    double operand1;
    double operand2;
    std::string exprStr;

};

#endif
