# Differentiation solver

'''Plan:
    1. First we convert a string representing the term to differenciate into a tree (Step 1)
    2. Then we use the tree to perform the differenciation (Step 2)
    3. Then we convert the tree into a string (combining like-terms along the way (Step 3)
'''

# imports
from tree import Tree
import latexify # may not need to import
import sympy as sp
import math # may not need
import numpy as np # may not need

''' Step 1: Status incomplete'''
# Convert from string to tree
def convertDerivativeExpressionToTree(expression):
    pass

'''Step 2: Status incomplete'''
# Differentiate using tree
    
def convertToDerivativeTree(tree):
    if tree.isLeaf():
        return tree.value
    else:
        pass
        # expressions 


'''tree to list version -- Kosbie said no'''
# def evalDerivativeTree(tree):
#     if tree.isLeaf():
#         return tree.value
#     else:
#         expressions = []
#         for child in tree.children:
#             expressions.append(evalDerivativeTree(child))
#         if tree.value == '+':
#             return sum(expressions)
#         elif tree.value == '*':
#             result = 1
#             for expression in expressions:
#                 result *= expression
#             return result
#         elif tree.value == '^':
#             return something

'''tree to tree version'''
def calculateDerivativeTree(tree):
    # operators = ['+', '-',  
    # Operator cases
    if tree.isLeaf():
        pass # do some stuff

    else:
        # do some calculations
        if tree.value == '+':
            finalTree = Tree('+')
            for child in tree.children:
                derivativeChild = calculateDerivativeTree(child)
                finalTree.addChild(derivativeChild)
            return finalTree
    
        if tree.value == '-':
            finalTree = Tree('-')
            for child in tree.children:
                derivativeChild = calculateDerivativeTree(child)
                finalTree.addChild(derivativeChild)
            return finalTree
        
        if tree.value == '*':
            finalTree = None
            for child in tree.children:
                if finalTree == None:
                    finalTree = child
                else:
                    finalTree = performProductRule(finalTree, child)
            return finalTree
    
        if tree.value == '/':
            numerator = None
            denominator = None
            for child in tree.children:
                if numerator == None:
                    numerator = child
                else:
                    denominator = child
            finalTree = performQuotientRule(numerator, denominator)
            return finalTree


def performProductRule(tree):
    pass

def performQuotientRule(numerator, denominator):
    pass
'''Step 3: Status almost complete'''
''' Idea:
    1. Convert tree to list
    2. Evaluate the list to LaTex
'''
# Convert tree to string in latex formatting
def convertTreeToLaTex(tree):
    operators = ['+', '-', '*', '^']
    listExpr = convertTreeToList(tree, operators)
    laTexExpr = convertListToLatex(listExpr, operators)
    return laTexExpr

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
    simplifiedExpr = sp.simplify(sp.sympify(exprString))
    laTexExpr = latexifyExpr(simplifiedExpr)
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


@latexify.expression
def latexifyExpr(expr):
    return expr

''' Test functions (need to write)'''
# Trees to test on!
def testingTreeToLaTex():
    t = Tree('+',
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
    assert(convertTreeToLaTex(t) == '2+5x^x+7x^7')

'''testing derivative calculator'''
def testingDerivativeCalc():
    tree1 = Tree('+',
                 Tree(5),
                 Tree('x'))
    derivativeTree = calculateDerivativeTree(tree1)
    print(convertTreeToLaTex(derivativeTree))

testingDerivativeCalc()