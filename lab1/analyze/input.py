def feb(x):
    if x==1:
        return 1
    else:
        return feb(x-1)+feb(x-2)

def do():
    for i in range(1,200):
        print 'num is '+i
str='''
haha
lalala
'''
feb(lambda x:x+1)

