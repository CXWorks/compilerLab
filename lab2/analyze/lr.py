def analyze(token):
    def getNext():
        i=0
        while True:
            yield i
            i+=1
    import pandas as pd
    from collections import deque

    from treelib import Tree,Node
    import re

    tokens=[]
    for l in token:
        s=re.split(r' ',l)
        tokens.append(s[0])
    tokens.append('$')
    test = deque(tokens)
    rr = {'r1': 'E=E+T', 'r2': 'E=T', 'r3': 'T=T*F', 'r4': 'T=F', 'r5': 'F=(E)', 'r6': 'F=i'}
    class CompiledError(StandardError):
        def __init__(self, arg):
            self.arg = arg
        def __str__(self):
            return self.arg
    state=[0]
    symbolic=['$']
    ast=[]
    table=pd.read_csv('table.csv',index_col=0,na_filter=False)
    ltest=len(test)
    while(len(test)!=0):
        if test[0] not in table.columns:
            raise CompiledError('%s, unrecognized token at %d' % (test[0],ltest-len(test)))
        ins=table.loc[state[-1],test[0]]
        if len(ins) == 0:
            raise CompiledError('%s complie failed at %d, unexpected token' % (test[0],ltest-len(test)))
        if ins[0] == 's':
            state.append(int(ins[1:]))
            tree=Tree()
            tree.create_node(test[0],getNext())
            ast.append(tree)
            symbolic.append(test.popleft())
        elif ins[0] == 'r':
            rule=rr[ins]
            print rule
            li=list(rule)
            li.reverse()
            temptree=[]
            for i in li:
                if i != '=' :
                    symbolic.pop()
                    state.pop()
                    temptree.append(ast.pop())
                else:
                    break
            symb=rule[:rule.find('=')]
            symbolic.append(symb)
            state.append(int(table.loc[state[-1],symbolic[-1]]))
            tree=Tree()
            ii=getNext()
            tree.create_node(symb,ii)
            for tri in temptree:
                tree.paste(ii,tri)
            ast.append(tree)
        elif ins == 'AC':
            print 'succeed'
            tree=ast.pop()
            tree.show()
            return
    raise CompiledError('%s compiled failed at %d, unexpected token' % (test[0],ltest-len(test)))

if __name__ == '__main__':
    import sys
    if len(sys.argv)<2:
        analyze(list('i+(i+i)*i'))
    else:
        t=sys.argv[1]
        f = open(t)
        li = f.readlines()

        analyze(li)



