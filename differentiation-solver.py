# Differentiation solver

'''Plan:
    1. First we convert a string representing the term to differenciate into a tree (Step 1)
    2. Then we use the tree to perform the differenciation (Step 2) -- almost done
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
            # it's a constant variable term
            return Tree(0)

    else:
        # do some calculations depending on the operator
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
            finalTree = Tree(0) # 0 is a placeholder
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
            # d/dx(sin(f(x))) = f'(x)*cos(f(x))

            for child in tree.children:
                functChild = child # functChild = f(x)
            finalTree = Tree('*')

            # f'(x) part
            coeff = calculateDerivativeTree(functChild)

            # f(x)
            innerPartOfFunction = functChild

            # cos(f(x)) part
            cosPartOfTree = Tree('cos')
            cosPartOfTree.addChild(innerPartOfFunction)
            
            finalTree.addChild(coeff)
            finalTree.addChild(cosPartOfTree)

            return finalTree
        
        if tree.value == 'cos':
            # d/dx(cos(f(x))) = -f'(x)*sin(f(x))

            for child in tree.children:
                functChild = child
            
            # f'(x)
            finalTree = Tree('*')
            unfactoredCoeff = calculateDerivativeTree(functChild)

            # but since d/dx(cos) --> -sin, we have to include -1 factor
            innerPartOfFunction = functChild
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
            innerPartOfFunction = functChild

            secPartOfTree = Tree('sec')
            secPartOfTree.addChild(innerPartOfFunction)
            
            # we add the sec part of tree twice since d/dx(tan) --> sec^2
            finalTree.addChild(coeff)
            finalTree.addChild(secPartOfTree)
            finalTree.addChild(secPartOfTree)

            return finalTree

        # below line of code is from AI
        raise ValueError(f"Unsupported operator: {tree.value}")


def performProductRule(finalTree, child):
    u = finalTree
    v = child
    uPrime = calculateDerivativeTree(u)
    vPrime = calculateDerivativeTree(v)
    result = Tree('+',
                  Tree('*',
                       u, vPrime),
                    Tree('*',
                         v, uPrime))
    return result

def performQuotientRule(numerator, denominator):
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
    if isinstance(base.value,int) or isinstance(base.value, float):
        if isinstance(power.value, int) or isinstance(power.value, float):
            return Tree(0)
        else:
            # case: k^f(x)
            result = Tree('*')
            coeff = Tree('ln')
            coeff.addChild(f'{base.value}')
            variableTree = Tree('*',
                                base, power)
            chainRuleTerm = calculateDerivativeTree(power)
            result.addChild(coeff)
            result.addChild(variableTree)
            result.addChild(chainRuleTerm)
            return result
    else:
        if isinstance(power.value,int) or isinstance(power.value, float):
            # case: f(x)^k
            newPower = power.value - 1

            coeff = power
            variableTerm = Tree('^',
                                base,
                                Tree(newPower))
            chainRuleTerm = calculateDerivativeTree(base)
            result = Tree('*',
                          coeff,
                          chainRuleTerm,
                          variableTerm)

            return result
        else:
            derivativeVariable = 'x' # hardcoded derivative variable for now
            if derivativeVariable in str(power.value):
                # case: f(x)^g(x)
                # d/dx(f(x)^g(x)) = f*g*(1/x)(f') + f*g'*ln(x)(f')
                f = Tree('^',
                         base,
                         power)
                g = power
                gPrime = calculateDerivativeTree(g)
                chainRuleTerm = calculateDerivativeTree(base)

                subFirstPart = Tree('/')
                subFirstPart.addChild(Tree(1))
                subFirstPart.addChild(Tree(f'{derivativeVariable}'))

                firstPart = Tree('*')
                firstPart.addChild(f)
                firstPart.addChild(g)
                firstPart.addChild(subFirstPart)
                firstPart.addChild(chainRuleTerm)

                subSecondPart = Tree('ln')
                subSecondPart.addChild(Tree(f'{derivativeVariable}'))

                secondPart = Tree('*')
                secondPart.addChild(f)
                secondPart.addChild(gPrime)
                secondPart.addChild(subSecondPart)
                firstPart.addChild(chainRuleTerm)

                result = Tree('+')
                result.addChild(firstPart)
                result.addChild(secondPart)
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

def performTrigLogPowerRule(base, power):
    firstPartOfExpr = performPowerRule(base,power)
    secondPartOfExpr = performPowerRule(base,1)
    finalTree = Tree('*')
    finalTree.addChild(firstPartOfExpr)
    finalTree.addChild(secondPartOfExpr)
    return finalTree

'''Step 3: Status complete'''
''' Idea:
    1. Convert tree to list
    2. Evaluate the list to LaTex
'''
# Converts a tree to a list
def convertTreeToList(tree, operators):
    if not isinstance(tree,Tree):
        print(f"value '{tree}' is Nonetype")
    if tree.isLeaf() and tree.value not in operators:
        return [tree.value]
    else:
        operator = tree.value
        finalExpr = []
        currBracket = []
        for child in tree.children:
            # The following two lines are from AI
            if not isinstance(child, Tree):
                raise ValueError(f"Invalid child node: {child}")
            if not operator.isalpha():
                childExpr = convertTreeToList(child,operators)
                finalExpr.append(childExpr)
                finalExpr.append(operator)
            else:
                # so operator is like sin or cos or ln
                innerTerm = convertTreeToList(child, operators)
                currBracket += [[operator, innerTerm], '*']
                finalExpr += currBracket
        return finalExpr[:-1]

def convertTreeToLatex(tree):
    operators = ['+', '-', '*', '^', 'ln', '/', 'sin', 'cos', 'tan', 'sec']
    exprList = convertTreeToList(tree, operators)
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

# I'm not sure if formatting acc works due to vscode limitations
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
                      Tree(3)))
    tree2 = Tree('/',
                 Tree(5),
                 Tree('^',
                      Tree('x'),
                      Tree('x')))
    
    tree3 = Tree('^',
                 Tree('x'),
                 Tree('a'))
    
    tree4 = Tree('sin',
                    Tree('cos',
                            Tree('^',
                                Tree('x'),
                                Tree('x'))))
    
    tree5 = Tree('*',
                 Tree('x'),
                 Tree('sin',
                    Tree('x')))
    
    tree6 = Tree('*',
                 Tree('cos',
                        Tree('x')),
                 Tree('-',
                        Tree('^',
                            Tree('tan',
                                 Tree('x')),
                            Tree(2)),
                        Tree(1)))
    
    tree7 = Tree('*',
                 Tree(2),
                 Tree('tan',
                      Tree('x')))
    
    tree8 = Tree('^',
                 Tree('tan',
                      Tree('x')),
                Tree(2))
    
    # trees 9 to 28 are generated by chatGPT

    tree9 = Tree('sin',
             Tree('+',
                  Tree('^',
                       Tree('x'),
                       Tree('x')),
                  Tree('cos',
                       Tree('*',
                            Tree('tan',
                                 Tree('x')),
                            Tree(3.14)))))

    tree10 = Tree('^',
                Tree('-',
                    Tree('cos',
                            Tree('^',
                                Tree('x'),
                                Tree(2))),
                    Tree('tan',
                            Tree('+',
                                Tree('x'),
                                Tree(1.5)))),
                Tree('/',
                    Tree('x'),
                    Tree(0.5)))

    tree11 = Tree('*',
                Tree('sin',
                    Tree('cos',
                            Tree('tan',
                                Tree('x')))),
                Tree('^',
                    Tree('+',
                            Tree('x'),
                            Tree(2.71)),
                    Tree(2)))

    tree12 = Tree('-',
                Tree('^',
                    Tree('x'),
                    Tree('^',
                            Tree('x'),
                            Tree('x'))),
                Tree('cos',
                    Tree('^',
                            Tree('x'),
                            Tree('+',
                                Tree(1),
                                Tree('x')))))

    tree13 = Tree('+',
                Tree('sin',
                    Tree('*',
                            Tree('tan',
                                Tree('x')),
                            Tree('^',
                                Tree('x'),
                                Tree(3)))),
                Tree('^',
                    Tree('cos',
                            Tree('x')),
                    Tree(0.5)))

    tree14 = Tree('/',
                Tree('^',
                    Tree('x'),
                    Tree('+',
                            Tree('x'),
                            Tree('x'))),
                Tree('-',
                    Tree('sin',
                            Tree('x')),
                    Tree('cos',
                            Tree('x'))))

    tree15 = Tree('tan',
                Tree('+',
                    Tree('^',
                            Tree('x'),
                            Tree('^',
                                Tree('x'),
                                Tree(2))),
                    Tree('sin',
                            Tree('/',
                                Tree('x'),
                                Tree(0.01)))))

    tree16 = Tree('*',
                Tree('^',
                    Tree('sin',
                            Tree('x')),
                    Tree('^',
                            Tree('x'),
                            Tree(2))),
                Tree('-',
                    Tree('cos',
                            Tree('x')),
                    Tree('tan',
                            Tree('x'))))

    tree17 = Tree('cos',
                Tree('-',
                    Tree('tan',
                            Tree('^',
                                Tree('+',
                                    Tree('x'),
                                    Tree(1.1)),
                                Tree(2))),
                    Tree('/',
                            Tree(3.14),
                            Tree('x'))))

    tree18 = Tree('^',
                Tree('cos',
                    Tree('*',
                            Tree('tan',
                                Tree('^',
                                    Tree('x'),
                                    Tree(2))),
                            Tree('x'))),
                Tree('sin',
                    Tree('x')))

    tree19 = Tree('+',
                Tree('^',
                    Tree('x'),
                    Tree('^',
                            Tree('x'),
                            Tree(2))),
                Tree('*',
                    Tree('tan',
                            Tree('cos',
                                Tree('x'))),
                    Tree('sin',
                            Tree('x'))))

    tree20 = Tree('-',
                Tree('^',
                    Tree('^',
                            Tree('x'),
                            Tree('x')),
                    Tree('x')),
                Tree('^',
                    Tree('tan',
                            Tree('x')),
                    Tree(0.33)))

    tree21 = Tree('*',
                Tree('^',
                    Tree('+',
                            Tree('sin',
                                Tree('x')),
                            Tree('cos',
                                Tree('x'))),
                    Tree('^',
                            Tree('x'),
                            Tree(2))),
                Tree('tan',
                    Tree('/',
                            Tree('x'),
                            Tree('^',
                                Tree('x'),
                                Tree(2)))))

    tree22 = Tree('^',
                Tree('sin',
                    Tree('cos',
                            Tree('^',
                                Tree('x'),
                                Tree('+',
                                    Tree('x'),
                                    Tree(1))))),
                Tree('/',
                    Tree(1.0),
                    Tree('x')))

    tree23 = Tree('-',
                Tree('tan',
                    Tree('+',
                            Tree('cos',
                                Tree('x')),
                            Tree('^',
                                Tree('x'),
                                Tree(2)))),
                Tree('sin',
                    Tree('*',
                            Tree('x'),
                            Tree('x'))))

    tree24 = Tree('cos',
                Tree('+',
                    Tree('^',
                            Tree('x'),
                            Tree('^',
                                Tree('x'),
                                Tree('x'))),
                    Tree('*',
                            Tree(0.5),
                            Tree('tan',
                                Tree('x')))))

    tree25 = Tree('*',
                Tree('^',
                    Tree('x'),
                    Tree('^',
                            Tree('x'),
                            Tree(2))),
                Tree('^',
                    Tree('sin',
                            Tree('x')),
                    Tree('cos',
                            Tree('x'))))

    tree26 = Tree('+',
                Tree('^',
                    Tree('tan',
                            Tree('^',
                                Tree('x'),
                                Tree(2))),
                    Tree('^',
                            Tree('x'),
                            Tree('x'))),
                Tree('^',
                    Tree('cos',
                            Tree('/',
                                Tree('x'),
                                Tree(0.1))),
                    Tree(3)))

    tree27 = Tree('-',
                Tree('^',
                    Tree('^',
                            Tree('x'),
                            Tree('x')),
                    Tree('^',
                            Tree('x'),
                            Tree(2))),
                Tree('^',
                    Tree('tan',
                            Tree('+',
                                Tree('x'),
                                Tree(1))),
                    Tree('sin',
                            Tree('x'))))

    tree28 = Tree('cos',
                Tree('+',
                    Tree('^',
                            Tree('x'),
                            Tree('x')),
                    Tree('tan',
                            Tree('cos',
                                Tree('^',
                                    Tree('x'),
                                    Tree('x'))))))
    
    treesList = [tree9, tree10, tree11, tree12, tree13, tree14, tree15, tree16, tree17, tree18, tree19, tree20, tree21, tree22, tree23, tree24, tree25, tree26, tree27, tree28]

    '''
    Trees to check:
    tree10 -- trig disappeared???
    tree11 -- trig disappeared???
    need to check tree12 onwards
    '''

    for index, testTree in enumerate(treesList):
        operators = ['+', '-', '*', '^', 'ln', '/', 'sin', 'cos', 'tan', 'sec']
        derivativeTree = calculateDerivativeTree(testTree)
        print(f''' 
              ----------------------------------------------------------------------------------------
              currTree: {index + 9}
              the derivative of {convertTreeToLatex(testTree)} is {convertTreeToLatex(derivativeTree)}
              ----------------------------------------------------------------------------------------''')
        # print(f'''
        #       ---------
        #       for debugging purposes:
        #       initial tree as list = {convertTreeToList(testTree, operators)}
        #       final tree as list = {convertTreeToList(derivativeTree, operators)}
        #       final tree as unsimplified expression = {convertListToString(convertTreeToList(derivativeTree, operators), 0)}
        #       --------''')

testingDerivativeCalc()