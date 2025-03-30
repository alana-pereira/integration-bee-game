# Differentiation solver

'''Plan:
    1. First we convert a string representing the term to differenciate into a tree
    2. Then we use the tree to perform the differenciation
    3. Then we convert the tree into a string (combining like-terms along the way
'''

# imports
from cmu_cpcs_utils import testFunction, Tree
import sympy as sp


# Convert from string to tree
# Differentiate using tree

# Convert tree to string in latex formatting
  ''' Idea:
          1. Convert tree to list
          2. Evaluate the list to LaTex
  '''

# Converts a tree to a list
def convertTreeToList(tree, operators):
    result = []
    if tree.isLeaf() and tree.value not in operators:
        return tree.value
    else:
        operator = tree.value
        finalExpr = []
        currBracket = []
        for child in tree.children:
            if child.value in operators:
                currBracket += [convertTreeToList(child,operators), operator]
            else:
                currBracket += [str(child.value), operator]
        finalExpr.extend(currBracket[:-1])
        return finalExpr

# Converts a list to LaTeX formatting (work in progress)
def convertListToLatex(exprList, operators):
    lengthOfExpr = getLengthOfExpr(exprList, i=0)
    exprString = convertListToString(exprList, 0)
    simplifiedExpr = simplifyExpr(exprString)
    laTexExpr = latexify(simplifiedExpr)
    return laTexExpr

def convertListToString(exprList, i):
    length = len(exprList)
    if i >= length:
        return ''
    else:
        term = exprList[i]
        if isinstance(term, list):
            termLength = len(term)
            exprWithBrackets = '(' + convertListToString(term, 0) + ')'
        else:
            exprWithBrackets = str(term)
    return exprWithBrackets + convertListToString(exprList, i+1)
            
def getLengthOfExpr(L, i=0):
    if i >= len(L):
        return 0
    term = L[i]
    if isinstance(term, list):
        count = getLengthOfExpr(term,i=0)
    else:
        count = 1
    return count + getLengthOfExpr(L, i+1)
            
def simplifyExpr(expression):
    ''' note:
        use len(operator)!!!
    '''
    
    # First distribute terms with brackets
    
    # add together all constant terms
    
    # simplify x+x
    
    # simplify x+kx
    
    # simplify x*x
    
    # simplify x*kx
    
    # simplify x*x^a
    
    # simplify x*x^x
    
    # Dictionary to collect like terms
    
    # Final expression!



# Trees to test on!
def testTreeToLaTex():
  t = t = Tree('+',
        Tree(2),
        Tree('*',
            Tree(5),
            Tree('^',
                Tree('x'),
                Tree('x'))),
        Tree('*',
            Tree(7),
            Tree('x'),
            Tree('^',
                Tree('x'),
                Tree(6))))
