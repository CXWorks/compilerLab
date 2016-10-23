# -*- coding: utf-8 -*-
reversed={'False':1,'class':2,'finally':3,'is':4,'return':5,'None':6,'continue':7,'for':8,'lambda':9,'try':10,
'True':11,'def':12,'from':13,'nonlocal':14,'while':15,
'and':16,'del':17,'global':18,'not':19,'with':20,
'as':21,'elif':22,'if':23,'or':24,'yield':25,'assert':26,'else':27,'import':28,'pass':29,
'break':30,'except':31,'in':32,'raise':33,'=':34,'/':35,'+':36,'-':37,'*':38,'!':39,'#':40,'%':41,'<':42,'>':43,'^':44,'~':45,
           '(':46,')':47,'[':48,']':49,'{':50,'}':51,'\'':52,'\'\'':53,'\'\'\'':54,':':55,';':56,'"""':57,'==':58,
          '!=':59,'+=':60,'-=':61,'/=':62,'*=':63,'%=':64,'>>':65,'<<':66,'>=':67,'<=':68}




def spilt(line):
    ans=[]
    s=0
    #check pace
    if line[s]==' ':
        while line[s]==' ':
            s+=1
        if s%4!=0:
            raise Exception('space error')
    while s<len(line):
        if (line[s]>='a' and line[s]<='z') or (line[s]>='A' and line[s]<='Z') or line[s]=='_': #words
            start=s
            while (line[s]>='a' and line[s]<='z') or (line[s]>='A' and line[s]<='Z') or (line[s]>='0' and line[s]<='9') or line[s]=='_':
                s+=1
                if s==len(line):
                    break
            ans.append([line[start:s],start,s+1])
            continue
        elif line[s] in [' ',';']:
            s+=1
            continue
        elif line[s] in ['+','-','*','/','%']:
            if line[s+1]=='=':
                ans.append([line[s:s+1],s,s+2])

                continue
            else:
                ans.append([line[s],s,s+1])
            s += 1
        elif line[s] in ['=','!']:
            if line[s+1] == '=':
                ans.append([line[s:s+2],s,s+2])
                s+=2
                continue
            elif line[s]=='=':
                ans.append([line[s],s,s+1])
                s+=1
                continue
            else:
                raise TypeError()
        elif  line[s]>='0' and line[s] <='9' :
            start=s
            while line[s]>='0' and line[s]<='9':
                s+=1
                if s==len(line):
                    ans.append([line[start:s],start,s+1])
                    return  ans
            if line[s] == '.':
                s+=1
                while line[s] >= '0' and line[s] <= '9':
                    s += 1
                    if s == len(line):
                        ans.append([line[start:s],start,s+1])
                        return ans
                ans.append([line[start:s],start,s+1])
                continue
            else:
                ans.append([line[start:s],start,s])
                continue
        elif line[s] in ['>','<',]:
            if line[s+1] == '=' or line[s+1]==line[s]:
                ans.append([line[s:s+1],s,s+2])
                s+=1
                continue
            else:
                ans.append([line[s],s,s+1])
                s+=1
                continue
        elif line[s]=='#':
            return ans
        elif line[s]=='\'' or line[s]=='"': #most difficult

            if line[s+1] != line[s] :
                start=s
                s += 1
                while line[s]!=line[start] and line[s-1]!='\\':
                    s+=1
                    if s==len(line):
                        ans.append([line[start:s],start,s+1])
                        return ans
                s+=1
                ans.append([line[start:s],start,s+1])
                continue
            elif s+2>=len(line) or  line[s+2] != line[s]:
                ans.append([line[s],s,s+1])
                ans.append([line[s+1],s+1,s+2])
                s+=2
                continue
            else:
                ans.append([line[s:s+3],s,s+4])
                s+=3
                continue
        elif line[s] in ['(',')','[',']','{','}',':',',','.']:
            ans.append([line[s],s,s+1])
            s+=1
        else:
            s+=1
    return ans




def parse(line):
    linum=1
    state=False
    for l in line:
        use=spilt(l)
        for val,sp,ep in use:
            if not state and val != '"""' and val !='\'\'\'':
                if val in reversed.keys():

                    yield val,reversed[val],linum,sp,ep
                else:
                    reversed[val]=len(reversed.keys())+1
                    yield val, reversed[val], linum, sp, ep
            elif not state:
                yield val,reversed[val],linum,sp,ep
                state=True
            elif state:
                if val == '"""' or val=='\'\'\'':

                    state=False
                    yield temp
                    yield val, reversed[val], linum, sp, ep
                else:
                    if 'temp' in locals().keys():
                        temp[0]=temp[0]+val
                        temp[4]=linum
                    else:
                        temp=[val, 0, 0, linum, linum]
        linum+=1
def correct(f):
    from tokenize import generate_tokens
    import StringIO
    l=f.readlines()
    str=''
    for s in l:
        str+=s
    for a,b,c,d,e in generate_tokens(StringIO.StringIO(str).readline):
        print a,b,c,d,e
if __name__ == '__main__':
    import sys
    import pandas as pd

    src='input.py'#sys.argv[1]
    file=open(src)
    correct(file)
    exit()
    tokens=[]
    index=['val','id','line','startPosition','endPosition']
    for val,index,li,sp,ep in parse(file.readlines()):
        tokens.append([val,index,li,sp,ep])
    df=pd.DataFrame(tokens)
    df=df.rename(columns={0:'val',1:'id',2:'line',3:'startPosition',4:'endPosition'})
    pd.DataFrame.to_csv(df,'output.csv')
    print df


