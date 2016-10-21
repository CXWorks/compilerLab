import networkx as nx
import matplotlib.pyplot as plt
def isChar(c):
    return (c>='a' and c<='z') or (c>='A' and c<='Z') or (c>='0' and c<='9')

def re2nfa(re):
    _op_={'.':6,'|':7,'(':0}
    #add .
    full=[]
    for i in range(len(re)):
        full.append(re[i])
        if re[i] not in _op_.keys() and i+1<len(re) and (isChar(re[i+1]) or re[i+1]=='('):
            full.append('.')
    full.append('$')
    # back
    back=[]
    symb=[]
    for c in full:
        if isChar(c):
            back.append(c)
        elif c=='(':
            while len(symb)!=0 and symb[len(symb)-1]!='(':
                back.append(symb.pop())
            symb.append('(')
        elif c==')':
            while symb[len(symb)-1]!= '(':
                back.append(symb.pop())
            symb.pop()
        elif c=='$':
            while len(symb)>0:
                back.append(symb.pop())
        elif c in ['*','+','?']:
            back.append(c)
        elif c in _op_.keys():
            while len(symb)>0 and _op_[symb[len(symb)-1]] >= _op_[c]:
                back.append(symb.pop())
            symb.append(c)
    del full,symb
    #build nfa
    print back
    stack=[]
    for c in back:
        if isChar(c):
            g=nx.DiGraph()
            g.add_edge(1,2,c=c)
            stack.append(g)
        elif c== '.':
            g1=stack.pop()
            g2=stack.pop()
            n=len(g1)
            g=nx.disjoint_union(g1,g2)
            g.add_edge(n-1,n,e='1')
            stack.append(g)
        elif c=='*':
            g=stack[len(stack)-1]
            n=len(g)
            g.add_edge(0,n-1,e='1')
            g.add_edge(n-1,0,e='1')
        elif c=='+':
            g = stack[len(stack)-1]
            n = len(g)
            g.add_edge(n - 1, 0, e='1')
        elif c=='?':
            g = stack[len(stack) - 1]
            n = len(g)
            g.add_edge(0, n - 1, e='1')
        elif c=='|':
            g1 = stack.pop()
            g2 = stack.pop()
            n = len(g1)
            g = nx.disjoint_union(g1, g2)
            g.add_edge(n - 1, n, e='1')
            stack.append(g)





if __name__ == '__main__':
    f=open('re')
    re2nfa(f.readline())
