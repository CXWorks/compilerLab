
relist=[]
code=[]

switch0={}
def case0(token):
    way={}
    way['a']=1
    way['b']=2
    way['+']=3
    if way.has_key(token):
        return way[token]
    else:
        return -1
switch0[0]=case0
def case1(token):
    way={}
    way['a']=1
    way['b']=2
    way['+']=3
    if way.has_key(token):
        return way[token]
    else:
        return -1
switch0[1]=case1
def case2(token):
    way={}
    way['a']=1
    way['b']=2
    way['+']=3
    if way.has_key(token):
        return way[token]
    else:
        return -1
switch0[2]=case2
def case3(token):
    way={}
    if way.has_key(token):
        return way[token]
    else:
        return -1206
switch0[3]=case3
relist.append(switch0)
def code0(yytext,start,end):
    print yytext,start,end

code.append(code0)

switch1={}
def case0(token):
    way={}
    way['a']=1
    way['b']=2
    if way.has_key(token):
        return way[token]
    else:
        return -1
switch1[0]=case0
def case1(token):
    way={}
    if way.has_key(token):
        return way[token]
    else:
        return -1206
switch1[1]=case1
def case2(token):
    way={}
    if way.has_key(token):
        return way[token]
    else:
        return -1206
switch1[2]=case2
relist.append(switch1)
def code1(yytext,start,end):
    print yytext,start,end

code.append(code1)




def next(str,i):
    while i<len(str) and str[i]==' ' :
        i+=1
    return i
if __name__ == '__main__':
    f=open('t.py')
    line=f.readlines()
    for l in line:
        if l[-1]!='\n':
            l+='\n'
        i=0
        while i<len(l) :
            i=next(l,i)
            start=i
            n=len(relist)
            state=[0]*n
            find=False
            while  i<len(l):
                j=0
                #do all the switch
                while j<len(state):
                    if state[j]==-1:
                        j+=1
                        continue
                    ans=relist[j][state[j]](l[i])
                    if ans == -1206:
                        find=True
                        break
                    elif ans == -1:
                        n-=1
                    state[j]=ans
                    j+=1
                if find :
                    #find
                    code[j](l[start:i],start,i)
                    break
                elif n==0 :
                    #not found
                    i+=1
                    break
                else:
                    i+=1






