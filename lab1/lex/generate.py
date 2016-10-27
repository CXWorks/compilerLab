import Cheetah.Template as tem
from test import re2dfa
def template(dic):
    return  tem.Template(file='template.tmpl',
                       searchList=[dic]).__str__()



def parseCXL(p):
    f=open(p)
    l=f.readlines()
    i=0
    while l[i][:2]!='#*':
        i+=1
    re=[]
    code=[]
    state=0# 0 for re 1 for code
    while i<len(l)-1:
        i+=1
        if l[i]=='\n':
            continue
        if l[i]=='*#':
            break
        if state==0:
            state=1
            re.append(l[i])
        else:
            state=0
            while l[i][:2]!='##':
                i+=1
            co=''
            i+=1
            while l[i][:2]!='##':
                co+=l[i]
                i+=1
            code.append(co)
    return [re,code]



if __name__ == '__main__':
    s='self.cxl'
    re,code=parseCXL(s)
    dfa=[]
    for r in re:
        dfa.append(re2dfa(r))
    re={}
    for i in range(len(dfa)):
        temp={'node':dfa[i][0],'edge':dfa[i][1]}
        re[i]=temp
    dic={'incl':s,'re':re,'code':code}
    ttt=template(dic)
    py=open('out.py','w')
    py.write(ttt)




