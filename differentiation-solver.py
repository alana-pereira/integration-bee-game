# Differentiation solver

'''Plan:
    1. First we convert a string representing the term to differenciate into a tree (Step 1) 
    2. Then we use the tree to perform the differenciation (Step 2) -- DONE
    3. Then we convert the tree into a string (combining like-terms along the way (Step 3) -- DONE
'''

# imports
from tree import Tree
import latexify # may not need to import
import sympy as sp
from sympy import symbols, pretty
import math # may not need
import numpy as np # may not need

''' Step 1: Status incomplete'''
# Convert from string to tree
def convertDerivativeExpressionToTree(expression):
    pass

'''Step 2: Status complete'''
def calculateDerivativeTree(tree):
    # operators = ['+', '-', '*', '^', 'ln', '/', 'sin', 'cos', 'tan', 'sec']
    derivativeVariable = 'x' # hardcoded for now
    # Operator cases
    if tree.isLeaf():
        if tree.value == derivativeVariable:
            return Tree(1)
        elif isinstance(tree.value,int) or isinstance(tree.value,float):
            return Tree(0)
        else:
            # probably a constant variable term
            return Tree(0)

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

        if tree.value == '^':
            # power rule!
            finalTree = Tree(0) # 0 is a placeholder -- dunno how to generate empty tree
            power = None
            base = None

            for child in tree.children:
                if base == None:
                    base = child
                elif power == None:
                    power = child
                else:
                    power = finalTree
                    base = None
                
                if (power != None) and (base != None):
                    
                    # next 2 lines are from AI
                    if not isinstance(base, Tree) or not isinstance(power, Tree):
                        raise ValueError(f"Invalid base or power: base={base}, power={power}")
                    
                    finalTree = performPowerRule(base, power)
            return finalTree
        
        if tree.value == 'ln':
            #ln(f) = f'/f = numerator/denominator
            denominator = tree
            numerator = calculateDerivativeTree(tree)
            finalTree = numerator/denominator
            return finalTree
        
        if tree.value == 'sin':
            for child in tree.children:
                functChild = child
            finalTree = Tree('*')
            coeff = innerDerivative = calculateDerivativeTree(functChild)
            innerPartOfFunction = tree

            cosPartOfTree = Tree('cos')
            cosPartOfTree.addChild(innerPartOfFunction)
            
            finalTree.addChild(coeff)
            finalTree.addChild(cosPartOfTree)

            return finalTree
        
        if tree.value == 'cos':
            for child in tree.children:
                functChild = child
            finalTree = Tree('*')
            unfactoredCoeff = innerDerivative = calculateDerivativeTree(functChild)
            # but since d/dx(cos) --> -sin, we have to include -1 factor
            innerPartOfFunction = tree
            coeff = Tree('*')
            coeff.addChild(Tree(-1))
            coeff.addChild(unfactoredCoeff)

            sinPartOfTree = Tree('sin')
            sinPartOfTree.addChild(innerPartOfFunction)
            
            finalTree.addChild(coeff)
            finalTree.addChild(sinPartOfTree)

            return finalTree
        
        if tree.value == 'tan':
            for child in tree.children:
                functChild = child
            finalTree = Tree('*')
            coeff = innerDerivative = calculateDerivativeTree(functChild)
            innerPartOfFunction = tree

            secPartOfTree = Tree('sec')
            secPartOfTree.addChild(innerPartOfFunction)
            
            # we add the sec part of tree twice since d/dx(tan) --> sec^2
            finalTree.addChild(coeff)
            finalTree.addChild(secPartOfTree)
            finalTree.addChild(secPartOfTree)

            return finalTree

        # below code is from AI
        raise ValueError(f"Unsupported operator: {tree.value}")


def performProductRule(finalTree, child):
    # print(f''' entered product rule''')
    u = finalTree
    v = child
    uPrime = calculateDerivativeTree(u)
    vPrime = calculateDerivativeTree(v)
    result = Tree('+',
                  Tree('*',
                       u, vPrime),
                    Tree('*',
                         v, uPrime))
    
    # print(f'result from product rule is {convertListToLatex(convertTreeToList(result, operators),operators)}')
    return result

def performQuotientRule(numerator, denominator):
    # print(f''' entered quotient rule''')
    u = numerator
    v = denominator
    uPrime = calculateDerivativeTree(u)
    vPrime = calculateDerivativeTree(v)
    numeratorDerivative = Tree('-',
                                Tree('*', v, uPrime),
                                Tree('*', u, vPrime))
    vSquared = Tree('^',
                    v, Tree(2))
    return Tree('/', numeratorDerivative, vSquared)

def performPowerRule(base, power):
    operators = ['+', '-', '*', '^', 'ln', '/', 'sin', 'cos', 'tan', 'sec']
    # print(f''' entered power rule
    #             base tree = {base}
    #             power tree = {power}''')
    if isinstance(base.value,int) or isinstance(base.value, float):
        # print('base is a number')
        if isinstance(power.value, int) or isinstance(power.value, float):
            # print('power is a number')
            return Tree(0)
        else:
            # print('power is NOT a number')
            result = Tree('*')
            coeff = f'ln({power.value})'
            variableTree = Tree('*',
                                base, power)
            result.addChild(coeff)
            result.addChild(variableTree)
            return result
    else:
        # print('base is NOT a number')
        if isinstance(power.value,int) or isinstance(power.value, float):
            # print('power is a number')
            newPower = power.value - 1

            coeff = power
            variableTerm = Tree('^',
                                base,
                                Tree(newPower))
            result = Tree('*',
                          coeff,
                          variableTerm)
            
            # print(f'result from power rule is {convertListToLatex(convertTreeToList(result, operators),operators)}')

            return result
        else:
            # print('power is NOT a number')
            derivativeVariable = 'x' # hardcoded derivative variable for now
            if derivativeVariable in str(power.value):
                # print(f'{derivativeVariable} is in power!')
                # d/dx(x^g(x)) = f*g*(1/x) + f*g'*ln(x)
                f = Tree('^',
                         base,
                         power)
                # print(f'f is {convertListToLatex(convertTreeToList(f, operators),operators)}')
                g = power
                # print(f'g is {convertListToLatex(convertTreeToList(g,operators),operators)}')
                gPrime = calculateDerivativeTree(g)
                # print(f"g' is {convertListToLatex(convertTreeToList(gPrime,operators),operators)}")

                # result = Tree('+',
                #               Tree('*',
                #                    f,
                #                    g,
                #                    '/',
                #                    Tree(derivativeVariable)),
                #                 Tree('*',
                #                      f,
                #                      gPrime,
                #                      Tree(f'ln{derivativeVariable}'))) # need to make ln an operator!

                subFirstPart = Tree('/')
                subFirstPart.addChild(Tree(1))
                subFirstPart.addChild(Tree(f'{derivativeVariable}'))

                firstPart = Tree('*')
                firstPart.addChild(f)
                firstPart.addChild(g)
                firstPart.addChild(subFirstPart)

                subSecondPart = Tree('ln')
                subSecondPart.addChild(Tree(f'{derivativeVariable}'))

                secondPart = Tree('*')
                secondPart.addChild(f)
                secondPart.addChild(gPrime)
                secondPart.addChild(subSecondPart)

                result = Tree('+')
                result.addChild(firstPart)
                result.addChild(secondPart)
                
                # print(f'''
                #       result after power rule as list {convertTreeToList(result, operators)}
                #       result after power rule as expr {convertListToString(convertTreeToList(result, operators),0)}
                #     result after power rule in latex format {convertListToLatex(convertListToString(convertTreeToList(result, operators),0), operators)}''')
                return result

            else:
                # x ^ constant --> coeff*x*newPower
                coeff = oldPower = power
                newPower = Tree('-',
                                oldPower,
                                Tree(1))
                result = Tree('*',
                              coeff,
                              Tree(derivativeVariable),
                              newPower)
                return result

'''Step 3: Status complete'''
''' Idea:
    1. Convert tree to list
    2. Evaluate the list to LaTex
'''
# Convert tree to string in latex formatting
# Try-exception part was given by AI
def convertListToLatex(exprList, operators):
    try:
        lengthOfExpr = getLengthOfExpr(exprList, i=0)
        exprString = convertListToString(exprList, 0)
        simplifiedExpr = sp.simplify(sp.sympify(exprString))
        laTexExpr = latexifyExpr(simplifiedExpr)
        return laTexExpr
    except Exception as e:
        print(f"Error in convertListToLatex: {repr(e)}")
        raise

# Converts a tree to a list
def convertTreeToList(tree, operators): # need to fix this!!!!
    # print('working on the tree:', tree) # may uncomment later
    # result = []
    if not isinstance(tree,Tree):
        print(f"value '{tree}' is Nonetype")
    if tree.isLeaf() and tree.value not in operators:
        # print('expression list comprises of following value:', tree.value)
        return [tree.value] # added brackets
    else:
        operator = tree.value
        print('curr operator:', operator) # main op
        finalExpr = []
        currBracket = []
        for child in tree.children:
            # The following two lines are from AI
            if not isinstance(child, Tree):
                raise ValueError(f"Invalid child node: {child}")
            # print('curr child is', child)
            # if child.value in operators:
                # need to simplify expr
            if not operator.isalpha():
                childExpr = convertTreeToList(child,operators)
                finalExpr.append(childExpr)
                finalExpr.append(operator)
            else:
                # so operator is like sin or cos or ln
                innerTerm = convertTreeToList(child, operators)
                print('inner term:', innerTerm)
                currBracket += [[operator, innerTerm], '*'] # need to check if this works
                print('to add', [[operator, innerTerm], '*'])
                print('after adding', currBracket)
        
            # finalExpr.extend(currBracket[:-1])
        print('final expr',finalExpr[:-1])
        return finalExpr[:-1]
        # print('added term = ', finalExpr)

    # print('tree-->list:', finalExpr)
    return finalExpr

# Converts a list to LaTeX formatting (work in progress)
def convertListToLatex(exprList, operators):
    lengthOfExpr = getLengthOfExpr(exprList, i=0)
    exprString = convertListToString(exprList, 0)
    simplifiedExpr = sp.simplify(sp.sympify(exprString))
    laTexExpr = latexifyExpr(simplifiedExpr)
    return laTexExpr

def convertTreeToLatex(tree):
    operators = ['+', '-', '*', '^', 'ln', '/', 'sin', 'cos', 'tan', 'sec']
    exprList = convertTreeToList(tree, operators)
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
    assert(convertTreeToLatex(t) == '2+5x^x+7x^7')

'''testing derivative calculator'''
def testingDerivativeCalc():
    tree1 = Tree('/',
                 Tree(5),
                 Tree('^',
                      Tree('x'),
                      Tree(-3)))
    tree2 = Tree('/',
                 Tree(5),
                 Tree('^',
                      Tree('x'),
                      Tree('x')))
    
    tree3 = Tree('^',
                 Tree('x'),
                 Tree('x'))
    
    tree4 = Tree('sin',
                    Tree('cos',
                            Tree('^',
                                Tree('x',
                                Tree('x')))))
    
    tree5 = Tree('*',
                 Tree('x'),
                 Tree('sin',
                    Tree('x')))
    treesList = [tree5]

    for testTree in treesList:
        operators = ['+', '-', '*', '^', 'ln', '/', 'sin', 'cos', 'tan', 'sec']
        derivativeTree = calculateDerivativeTree(testTree)
        print(f'initial tree is {convertListToString(convertTreeToList(testTree, operators), 0)}')
        print(f'derivative tree is {convertTreeToLatex(derivativeTree)}')
        print(f'''
              ---------
              for debugging purposes:
              initial tree as list = {convertTreeToList(testTree, operators)}
              final tree as list = {convertTreeToList(derivativeTree, operators)}
              final tree as unsimplified expression = {convertListToString(convertTreeToList(derivativeTree, operators), 0)}
              --------''')

testingDerivativeCalc()