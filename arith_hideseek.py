from itertools import count, product
from pyparsing import Literal,Word,ParseException, infixNotation, opAssoc, ParseResults
import operator
from math import floor
#Python3 code. Requires pyparsing module (pip install pyparsing)

################################################################################
#  Formula parser, using PyParsing
################################################################################

nonzero_nums = "123456789"
nums = "0" + nonzero_nums

def make_parser():
    #Disallow numbers starting from 0, except 0 itself
    integer = Literal("0") | Word( nonzero_nums, nums )
    
    plus, minus, mult, div, expop, k  = map(Literal, "+-*/^k")
    return infixNotation( k | integer,
                          [(minus, 1, opAssoc.RIGHT),
                           (expop, 2, opAssoc.RIGHT),
                           (mult|div,   2, opAssoc.LEFT),
                           (plus|minus, 2, opAssoc.LEFT)])

__parser = make_parser()

def parse( s ): return __parser.parseString( s, parseAll=True )

def power(x, y):
    """Power with stricter evaluation rules"""
    if x == 0:
        if y == 0: raise ValueError("0^0")
    elif x < 0:
        if y != int(y): raise ValueError("non-integer power of negative")
    return x ** y

# map operator symbols to corresponding arithmetic operations
opn = { "+" : operator.add,
        "-" : operator.sub,
        "*" : operator.mul,
        "/" : operator.truediv,
        "^" : power }

def evaluate( result, k ):
    """Evaluate parsed formula"""
    if result == "k":
        return k
    elif isinstance(result, ParseResults):
        n = len(result)
        if n == 1: return evaluate( result[0], k )
        elif n == 2:
            assert result[0] == "-"
            return -evaluate(result[1], k)
        else:
            r = evaluate( result[0], k )
            for i in range(1, n, 2):
                r = opn[ result[i] ](r, evaluate( result[i+1], k ))
            return r
    else:
        return int(result, len(nums) )

################################################################################
#  Formula enumeration
################################################################################
def evaluate_safe( s, k ):
    try:
        return evaluate(s,k)
    except (ZeroDivisionError, ValueError):
        return 0
    except OverflowError:
        #can't really calculate the value.
        return float("NaN") 
    
def all_strings( alphabet ):
    for n in count(1):
        for s in product(alphabet, repeat=n):
            yield ''.join(s)

def all_formulas():
    """Generate pairs: formula, parsed formula"""
    for f in all_strings(nums + '+-*/^()k'):
        try:
            yield f, parse( f )
        except ParseException:
            pass        

def angel_sequence():
    for i, (f, f_parsed) in enumerate(all_formulas()):
        yield floor(evaluate_safe(f_parsed, i+1))

def plot_angel():
    from matplotlib import pyplot as pp
    from itertools import islice
    n = 10000
    print ("Calculating angel sequence for {n} steps...".format(**locals()))
    
    def try_float(x):
        try:
            return float(x)
        except Exception:
            return float("NaN")

    ks=[]
    ys = []
    stops = []
    for i, (f, f_parsed) in enumerate(islice(all_formulas(), n )):
        y = floor(evaluate_safe(f_parsed, i+1))
        try:
            ys.append(float(y))
            ks.append(i+1)
        except Exception:
            stops.append( i+1, f )
    
    print ("Plotting result")
    pp.semilogy( ks, ys, "*" )
    pp.show()
    
if __name__=="__main__":
    #plot_angel()
    
    for i, (f, f_parsed) in enumerate(all_formulas()):
        fx = floor(evaluate_safe(f_parsed, i+1))
        print ("{k}\t{f}\t{fx}".format(k=i+1, f=f, fx=fx))

    
