###########################
# Tree implementation (Tree class)
###########################

class Tree:
    def __init__(self, value, *children):
        self.value = value
        self.children = children

    def __repr__(self):
        return self.toString()

    def __eq__(self, other):
        return (isinstance(other, Tree) and
                (self.value == other.value) and
                (len(self.children) == len(other.children)) and
                (all([myChild == otherChild for myChild,otherChild in zip(self.children, other.children)])))

    def isLeaf(self):
        return len(self.children) == 0

    def addChild(self, child):
        assert(isinstance(child, Tree))
        if self._containsTree(child):
            raise Exception('The child tree is already in this tree.')
        self.children += (child,)

    def removeChild(self, child):
        assert(child in self.children)
        i = self.children.index(child)
        self.children = self.children[:i] + self.children[i+1:]

    def _containsTree(self, Tree):
        if self is Tree:
            return True
        for child in self.children:
            if child._containsTree(Tree):
                return True
        return False

    def toString(self, indent=0):
        base = f'{" "*indent}Tree({repr(self.value)}'
        if self.isLeaf():
            return base + ')'
        else:
            lines = [base + ',']
            for i in range(len(self.children)):
                child = self.children[i]
                lines.append(child.toString(indent+5))
                if i < len(self.children)-1:
                    lines[-1] += ','
            lines.append(f'{" "*indent})')
            return '\n'.join(lines)

###########################
# testTreeClass
###########################

def testTreeClass():
    print('Testing Tree class...', end='')

    # Construct a tree with its children in the constructor:

    tree0 = Tree(1,
                 Tree(2,
                      Tree(4)
                      ),
                 Tree(3)
                )
    assert(str(tree0) == '''\
Tree(1,
     Tree(2,
          Tree(4)
     ),
     Tree(3)
)''')

    # Construct a tree and then add its children with addChild:

    tree1 = Tree(1)
    tree2 = Tree(2)
    tree3 = Tree(3)
    tree4 = Tree(4)
    tree1.addChild(tree2)
    tree2.addChild(tree4)
    tree1.addChild(tree3)
    assert(tree0 == tree1)

    # removeChild:

    tree1.removeChild(tree2)

    assert(str(tree1) == '''\
Tree(1,
     Tree(3)
)''')

    assert(str(tree2) == '''\
Tree(2,
     Tree(4)
)''')

    assert(tree1 != tree0)

    print('Passed!')

if __name__ == '__main__':
    testTreeClass()