from combinatorics import *
import re
import cProfile

def test(n, ans):
    floated = [float(i) for i in n]
    inted = [int(i) if i.is_integer() else i for i in floated]
    combi = Combinatorics(inted)
    print combi.evaluate(ans, up_to=None, randomise=False, max_write_size=500000000)

def getValidList(l):
    numbers = re.findall(r'\d+(?:\.\d*)?', l)
    return numbers if len(numbers) != 0 else None

def getValidNumber(n):
    number = re.findall(r'\d+(?:\.\d*)?', n)
    return float(number[0]) if len(number) != 0 else None

def getNumbersFromUser():
    list_input = raw_input('Enter any number of numbers (eg. 1,2.5, 3): ')
    list_input = getValidList(list_input)
    if list_input is None:
        print 'Invalid input entered.'
        return None

    ans_input = raw_input('Enter the target value to be achieved: ')
    ans_input = getValidNumber(ans_input)
    if ans_input is None:
        print 'Invalid input entered.'
        return None

    return list_input, ans_input
    
def main():
    while True:
        try:
            # n, ans = getNumbersFromUser()
            test(*getNumbersFromUser())
            # cProfile.run("test([1, 2, 3, 4, 5], 24)")
            print
            
        except MemoryError:
            print 'memory error'
        print
        
main()
# cProfile.run("test([1,2,3,4,5], 24)")
#test(['1','2','3','5'], 24)

