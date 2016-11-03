def analyze():
    def getNext():
        i=0
        while True:
            yield i
            i+=1
    import pandas as pd
    from collections import deque
    import sys
    from treelib import Tree,Node
    if len(sys.argv)<2:
        t='table.csv'
    else:
        t=sys.argv[1]
    test = deque(list('i+(i+i)*$'))
    rr = {'r1': 'E=E+T', 'r2': 'E=T', 'r3': 'T=T*F', 'r4': 'T=F', 'r5': 'F=(E)', 'r6': 'F=i'}
    class CompiledError(StandardError):
        def __init__(self, arg):
            self.arg = arg
        def __str__(self):
            return self.arg
    state=[0]
    symbolic=['$']
    ast=[]
    table=pd.read_csv(t,index_col=0,na_filter=False)
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
    analyze()


# data=[('s5','','','s4','','',1,2,3),
#       ('','s6','','','','AC','','',''),
#       ('','r2','s7','','r2','r2','','',''),
#       ('','r4','r4','','r4','r4','','',''),
#       ('s5','','','s4','','',8,2,3),
#       ('','r6','r6','','r6','r6','','',''),
#       ('s5','','','s4','','','',9,3),
#       ('s5','','','s4','','','','',10),
#       ('','s6','','','s11','','','',''),
#       ('','r1','s7','','r1','r1','','',''),
#       ('','r3','r3','','r3','r3','','',''),
#       ('','r5','r5','','r5','r5','','','')]
#
# index=[x for x in range(12)]
# columns=['i','+','*','(',')','$','E','T','F']
# table=pd.DataFrame(data=data,index=index,columns=columns)
# print table
# pd.DataFrame.to_csv(table,'table.csv')
