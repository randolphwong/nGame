#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <functional>
#include <chrono>
#include <sstream>
#include "ExprTree.h"

using std::cin;
using std::cout;
using std::endl;
using std::map;
using std::vector;
using std::istream;
using std::copy;
using std::cin;
using namespace std::chrono;

typedef vector<vector<double> >::const_iterator vvd_iter;

std::string operators = "*+/-";

vector<double>& getNumberSequence(istream& inStream, vector<double>& num_vector) {
    std::string input;
    std::getline(inStream, input);
    std::istringstream parser(input);
    double number;
    while (parser >> number) {
        num_vector.push_back(number);
    }
    return num_vector;
}

vector<vector<double> >& getCombination(const vector<double>& num_vector, int choice, vector<vector<double> >& combination) {
    if (choice == 0) return combination;
    if (choice == 1) {
        for (vector<double>::const_iterator it = num_vector.begin(); it != num_vector.end(); ++it) {
            combination.push_back(vector<double>(1, *it));
        }
        return combination;
    }
    for (vector<double>::size_type i = 0; i != num_vector.size(); ++i) {
        vector<vector<double> > combis;
        combis = getCombination(vector<double>(num_vector.begin() + i + 1, num_vector.end()), choice - 1, combis);
        for (vector<vector<double> >::const_iterator it = combis.begin(); it != combis.end(); ++it) {
            vector<double> first_num = vector<double>(1, num_vector[i]);
            copy(it->begin(), it->end(), std::back_inserter(first_num));
            combination.push_back(first_num);
        }
    }
    return combination;
}

void getAllCombination(const vector<double>& num_seq, vector<vector<double> >& combinations) {
    for (std::size_t i = 1; i != num_seq.size(); ++i) {
        getCombination(num_seq, i, combinations);
    }
}

void setPartition(const vector<double>& num_seq, vector<vector<double> >& part1, vector<vector<double> >& part2) {
    for (std::size_t i = 1; i != num_seq.size(); ++i) {
        getCombination(num_seq, i, part1);
    }

    for (vvd_iter combination1 = part1.begin(); combination1 != part1.end(); ++combination1) {
        vector<double> combination2;
        std::set_difference(num_seq.begin(), num_seq.end(), combination1->begin(), combination1->end(), std::back_inserter(combination2));
        part2.push_back(combination2);
    }
}

vector<ExprTree>& findNonRedundantExprTree(const vector<double>& num_seq, vector<ExprTree>& trees) {
    if (num_seq.size() == 1) {
        trees.push_back(ExprTree(num_seq[0]));
        return trees;
    }
    vector<vector<double> > part1, part2;
    setPartition(num_seq, part1, part2);
    // loop through all operators
    for (std::string::size_type op = 0; op != operators.length(); ++op) {
        vector<double> part1_old;
        for (vector<vector<double> >::size_type i = 0; i != part1.size(); ++i) {
            if (part2[i] == part1_old) break;
            part1_old = part1[i];
            vector<ExprTree> all_expr1, all_expr2;
            findNonRedundantExprTree(part1[i], all_expr1);
            findNonRedundantExprTree(part2[i], all_expr2);
            for (vector<ExprTree>::const_iterator expr1 = all_expr1.begin(); expr1 != all_expr1.end(); ++expr1) {
                for (vector<ExprTree>::const_iterator expr2 = all_expr2.begin(); expr2 != all_expr2.end(); ++expr2) {
                    trees.push_back(ExprTree(operators[op], *expr1, *expr2));
                    if (op > 1) trees.push_back(ExprTree(operators[op], *expr2, *expr1));
                }
            }
        }
    }
    return trees;
}

vector<ExprTree>& findAllExprTree(const vector<double>& num_seq, vector<ExprTree>& trees) {
    if (num_seq.size() == 1) {
        trees.push_back(ExprTree(num_seq[0]));
        return trees;
    }
    vector<vector<double> > part1, part2;
    setPartition(num_seq, part1, part2);
    // loop through all operators
    for (std::string::size_type op = 0; op != operators.length(); ++op) {
        vector<double> part1_old;
        for (vector<vector<double> >::size_type i = 0; i != part1.size(); ++i) {
            if (part2[i] == part1_old) break;
            part1_old = part1[i];
            vector<ExprTree> all_expr1, all_expr2;
            findAllExprTree(part1[i], all_expr1);
            findAllExprTree(part2[i], all_expr2);
            for (vector<ExprTree>::const_iterator expr1 = all_expr1.begin(); expr1 != all_expr1.end(); ++expr1) {
                for (vector<ExprTree>::const_iterator expr2 = all_expr2.begin(); expr2 != all_expr2.end(); ++expr2) {
                    trees.push_back(ExprTree(operators[op], *expr1, *expr2));
                    trees.push_back(ExprTree(operators[op], *expr2, *expr1));
                }
            }
        }
    }
    return trees;
}


int main() {
    cout << "Enter number sequence (separated by space): ";

    vector<double> num_seq;
    num_seq = getNumberSequence(cin, num_seq);

    cout << "Enter target value: ";
    
    double target;

    cin >> target;
 
    // performance check start
    high_resolution_clock::time_point t1 = high_resolution_clock::now();

    //vector<double> exprs;
    //exprs = findNonRedundantExprTree(num_seq, exprs);
    vector<ExprTree> exprs;
    exprs = findNonRedundantExprTree(num_seq, exprs);

    // performance check end
    high_resolution_clock::time_point t2 = high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count();

    // print solutions found
   
    std::cout << "Showing first 10 solutions (if any)." << std::endl;
    int soln_count = 0;
    for (vector<ExprTree>::const_iterator expr = exprs.begin(); expr != exprs.end(); ++expr) {
        if (std::abs(expr->eval() - target) < 0.01) {
            if (soln_count <= 10)
                std::cout << expr->str() << std::endl;
            ++soln_count;
        }
    }
    
    cout << "Duration for operations: " << (duration / 1000000.) << "s" << endl;
    cout << "Number of expressions enumerated: " << exprs.size() << endl;
    cout << "Number of solutions found: " << soln_count << endl;


    cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    cin.clear();
    cin.get();
    return 0;
}
