
relist=[]
code=[]

switch0={}
def case0(token):
    way={}
    way['1']=1
    way['0']=1
    way['3']=1
    way['2']=1
    if way.has_key(token):
        return way[token]
    else:
        return -1
switch0[0]=case0
def case1(token):
    way={}
    way['1']=1
    way['0']=1
    way['3']=1
    way['2']=1
    if way.has_key(token):
        return way[token]
    else:
        return -1206
switch0[1]=case1
relist.append(switch0)
def code0(yytext,start,end):
    print yytext,start,end

code.append(code0)

switch1={}
def case0(token):
    way={}
    way['a']=1
    way['c']=1
    way['b']=1
    if way.has_key(token):
        return way[token]
    else:
        return -1
switch1[0]=case0
def case1(token):
    way={}
    way['a']=1
    way['c']=1
    way['b']=1
    if way.has_key(token):
        return way[token]
    else:
        return -1206
switch1[1]=case1
relist.append(switch1)
def code1(yytext,start,end):
    print yytext,start,end

code.append(code1)

switch2={}
def case0(token):
    way={}
    way['=']=1
    if way.has_key(token):
        return way[token]
    else:
        return -1
switch2[0]=case0
def case1(token):
    way={}
    if way.has_key(token):
        return way[token]
    else:
        return -1206
switch2[1]=case1
relist.append(switch2)
def code2(yytext,start,end):
    print yytext,start,end

code.append(code2)




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
                    if state[j]==-1 or state[j]==-2:
                        j+=1
                        continue
                    ans=relist[j][state[j]](l[i])
                    if ans == -1:
                        n-=1
                    state[j]=ans
                    j+=1
                k=0
                for k in range(len(state)):
                    st=state[k]
                    if st == -1:
                        continue
                    elif st==-1206 and n>1:
                        state[k]=-2
                        n-=1
                    elif st==-1206 and n==1:
                        find=True
                        break
                if find :
                    #find
                    code[k](l[start:i],start,i)
                    break
                elif n==0 :
                    #not found
                    i=start+1
                    break
                else:
                    i+=1






