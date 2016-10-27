import networkx as nx
from collections import deque


def re2dfa(re):
    def isChar(c):
        return (c>='a' and c<='z') or (c>='A' and c<='Z') or (c>='0' and c<='9')
    way=[]
    def re2nfa(re):
        _op_={'.':6,'|':7,'(':10}
        #add .
        full=[]
        skip=False
        for i in range(len(re)):
            if skip:
                skip=False
                continue
            full.append(re[i])
            if re[i]=='\\':
                i+=1
                full.append(re[i])
                skip=True
            if re[i] not in _op_.keys() and i+1<len(re) and (isChar(re[i+1]) or re[i+1]=='(' or re[i+1]=='\\'):
                full.append('.')
        full.append('$')
        # back
        back=[]
        symb=[]
        skip=False
        for i in range(len(full)):
            if skip:
                skip=False
                continue
            c=full[i]
            if isChar(c):
                back.append(c)
                if c not in way:
                    way.append(c)
            elif c==')':
                while symb[len(symb)-1]!= '(':
                    back.append(symb.pop())
                symb.pop()
            elif c=='$':
                while len(symb)>0:
                    back.append(symb.pop())
            elif c in ['*','+','?']:
                back.append(c)
            elif c =='\\':
                back.append(c)
                i+=1
                back.append(full[i])
                skip=True
                if full[i] not in way:
                    way.append(full[i])
            elif c in _op_.keys():
                while len(symb)>0 and symb[len(symb)-1]!='(' and _op_[symb[len(symb)-1]] >= _op_[c]:
                    back.append(symb.pop())
                symb.append(c)
        #build nfa
        stack=[]
        skip=False
        for i in range(len(back)):
            if skip:
                skip=False
                continue
            c=back[i]
            if isChar(c):
                g=nx.DiGraph()
                g.add_edge(0,1,c=c)
                stack.append(g)
            elif c=='\\':
                i+=1
                g=nx.DiGraph()
                g.add_edge(0,1,c=back[i])
                stack.append(g)
                skip=True
            elif c== '.':
                g2=stack.pop()
                g1=stack.pop()
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
                n1 = len(g1)
                n2 = len(g2)
                s=nx.DiGraph()
                s.add_node(0)
                s1=nx.disjoint_union(s,g1)
                s1.add_edge(0,1,e='1')
                e=nx.DiGraph()
                e.add_node(0)
                e1=nx.disjoint_union(g2,e)
                e1.add_edge(n2-1,n2,e='1')
                ans=nx.disjoint_union(s1,e1)
                ans.add_edge(0,n1+1,e='1')
                ans.add_edge(n1,n1+n2+1,e='1')
                stack.append(ans)
        return stack.pop()


    def findClo(g,node):
        ans=[node]
        #dfs
        stack=[node]
        while len(stack)>0:
            n=stack.pop()
            edge = g.edge[n]
            for no,dic in edge.items():
                if no not in ans and dic.has_key('e'):
                    stack.append(no)
                    ans.append(no)
        return ans

    def findWay(g,ns,w):
        ans=[]
        for n in ns:
            edge=g.edge[n]
            for no,dic in edge.items():
                if no not in ans and dic.has_key('c') and dic['c']==w:
                    #find clo
                    temp=findClo(g,no)
                    ans.extend(temp)
        return ans
    def minDFA(node,index):
        ans=[]
        log=[]
        for i in range(len(node)):
            n=node[i]
            if n in log:
                continue
            nto=index[n].values()
            notin=[x for x in nto if x not in node]
            if len(notin)>0 :
                ans.append([n])
                continue
            t=[n]
            for j in range(i+1,len(node)):
                jto=index[node[j]].values()
                if nto==jto and len(nto)!=0:
                    t.append(node[j])
                    log.append(node[j])
            ans.append(t)
        return ans

    def delnode(n,conn,t,to):
        del conn[n]
        t[to].extend([x for x in t[n] if x not  in t[to]])
        del t[n]
        for k,v in conn.items():
            if k != n :
                for w in way:
                    if v.has_key(w) and v[w]==n :
                        v[w]=to
        return conn



    def nfa2dfa(nfa):
        table={}
        #init
        t=findClo(nfa,0)
        t.sort()
        table[0]=t
        conn={}
        queue=deque([0])
        while len(queue)>0:
            n=queue.popleft()
            n2c={}
            n_n=table[n]
            for c in way:
                te=findWay(nfa,n_n,c)
                if len(te)==0:
                    continue
                te.sort()
                if te not in table.values():
                    idd=len(table)
                    table[idd]=te
                    queue.append(idd)
                else:
                    idd=table.keys()[table.values().index(te)]
                n2c[c]=idd
            conn[n]=n2c
        #minimise
        s=[]
        e=[]
        for k,v in table.items():
            if len(nfa.node)-1 in v:
                e.append(k)
            else:
                s.append(k)
        s2=minDFA(s,conn)

        e2=minDFA(e,conn)
        s2.extend(e2)
        for l in s2:
            if len(l) == 1:
                continue
            for i in range(1,len(l)):
                conn=delnode(l[i],conn,table,l[0])
        #build graph
        g=nx.DiGraph()
        for k,v in table.items():

            g.add_node(k)
            if len(nfa.node) - 1 in v:
                g.node[k]['e']=1
        for node,di in conn.items():
            for c,t in di.items():
                g.add_edge(node,t,c=c)
        return g

    nfa = re2nfa(re)
    g = nfa2dfa(nfa)
    return [g.node,g.edge]





if __name__ == '__main__':
    print  re2dfa('function')