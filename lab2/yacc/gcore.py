import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import re
import pandas as pd
from first_follow import first_follow
way=['$']
noterminal = ['$$']

def G2nfa(G):
    coll=[]
    for g in G:
        li=re.split(r' ',g)
        if '|' in li :
            h=li[:li.index('->')+1]
            dli=li[li.index('->')+1:]
            t=[]
            for dg in dli:
                if dg == '|' :
                    coll.append(h+t)
                    t=[]
                else:
                    t.append(dg)
            coll.append(h+t)
        else:
            coll.append(li)
    coll.insert(0,['$$','->',coll[0][0]])
    g_s=[]
    for l in coll:
        g=nx.DiGraph()
        ii=i=0
        while i < len(l):
            if l[i] == '->' :
                i+=1
                continue
            co=l[:]
            if i < l.index('->'):
                co.insert(l.index('->')+1,'.')
                if l[i] not in noterminal :
                    noterminal.append(l[i])
            else:
                co.insert(i+1,'.')
            if l[i] not  in way:
                way.append(l[i])
            g.add_node(ii,v=co)
            i+=1
            ii+=1

        for j in range(i-2):
            g.add_edge(j,j+1, c=l[j+2])
        g_s.append(g)
    # deal with nfa
    leninex=[0]*len(g_s)
    header=['a']*len(g_s)
    for i in range(len(leninex)):
        leninex[i]=len(g_s[i].node)
        header[i]=g_s[i].node[0]['v'][0]
    nfa=nx.DiGraph()
    for g in g_s:
        nfa=nx.disjoint_union(nfa,g)
    for sn,list in nfa.edge.items():
        for en,char in list.items():
            if char['c'] in header:
                for j in range(len(header)):
                    if header[j]==char['c']:
                        nodin=sum(leninex[:j])
                        nfa.add_edge(sn,nodin,e=1)
    nfa.add_node(len(nfa.node),f=1)
    for j in range(1,len(leninex)+1):
        to=sum(leninex[:j])
        nfa.add_edge(to-1,len(nfa.node)-1,e=1)
    return nfa,coll
def findClo(g, node):
    ans = [node]
    # dfs
    stack = [node]
    while len(stack) > 0:
        n = stack.pop()
        edge = g.edge[n]
        for no, dic in edge.items():
            if no not in ans and dic.has_key('e'):
                stack.append(no)
                ans.append(no)
    return ans


def findWay(g, ns, w):
    ans = []
    for n in ns:
        edge = g.edge[n]
        for no, dic in edge.items():
            if no not in ans and dic.has_key('c') and dic['c'] == w:
                # find clo
                temp = findClo(g, no)
                ans.extend(temp)
    return ans


def minDFA(node, index):
    ans = []
    log = []
    for i in range(len(node)):
        n = node[i]
        if n in log:
            continue
        nto = index[n].values()
        notin = [x for x in nto if x not in node]
        if len(notin) > 0:
            ans.append([n])
            continue
        t = [n]
        for j in range(i + 1, len(node)):
            jto = index[node[j]].values()
            if nto == jto and len(nto) != 0:
                t.append(node[j])
                log.append(node[j])
        ans.append(t)
    return ans


def delnode(n, conn, t, to):
    del conn[n]
    t[to].extend([x for x in t[n] if x not in t[to]])
    del t[n]
    for k, v in conn.items():
        if k != n:
            for w in way:
                if v.has_key(w) and v[w] == n:
                    v[w] = to
    return conn


def nfa2dfa(nfa):
    table = {}
    # init
    t = findClo(nfa, 0)
    t.sort()
    table[0] = t
    conn = {}
    queue = deque([0])
    while len(queue) > 0:
        n = queue.popleft()
        n2c = {}
        n_n = table[n]
        for c in way:
            te = findWay(nfa, n_n, c)
            if len(te) == 0:
                continue
            te.sort()
            if te not in table.values():
                idd = len(table)
                table[idd] = te
                queue.append(idd)
            else:
                idd = table.keys()[table.values().index(te)]
            n2c[c] = idd
        conn[n] = n2c
    print table
    # minimise
    s = []
    e = []
    for k, v in table.items():
        if len(nfa.node) - 1 in v:
            e.append(k)
        else:
            s.append(k)
    s2 = minDFA(s, conn)

    e2 = minDFA(e, conn)
    s2.extend(e2)
    for l in s2:
        if len(l) == 1:
            continue
        for i in range(1, len(l)):
            conn = delnode(l[i], conn, table, l[0])

    # build graph
    g = nx.DiGraph()
    for k, v in table.items():

        g.add_node(k)
        if len(nfa.node) - 1 in v:
            g.node[k]['e'] = 1
    for node, di in conn.items():
        for c, t in di.items():
            # g.add_edge(node,t,)
            if g.has_edge(node, t):
                g.edge[node][t]['c'].append(c)
            else:
                g.add_edge(node, t, c=[c])
    return g

def follow():
    pass


def generateTable(g):
    data=[]
    for sn,list in g.edge.items():
        item={}
        for en,k in list.items():
            for c,l in k.items():
                for it in l:
                    if it =='$':
                        continue
                    if it not in noterminal:
                        word="s"+str(en)
                    else:
                        word=int(en)
                    item[it]=word
        data.append(item)

    df=pd.DataFrame(data)
    print df



if __name__ == '__main__':

    g,coll=G2nfa(['s -> s + t','s -> t','t -> t * f','t -> f','f -> ( s )','f -> i'])
    print coll
    first_follow(coll)
    # print coll
    # print g.edge
    # gg=nfa2dfa(g)
    # generateTable(gg)
