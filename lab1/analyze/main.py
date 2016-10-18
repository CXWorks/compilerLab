# -*- coding: utf-8 -*-
from token import NAME
from tokenize import generate_tokens, untokenize
from StringIO import StringIO

source = """def x(y):
    b = 2
    if y == b:
        foo(y)"""
result = []
tokens = generate_tokens(StringIO(source).readline)
for toknum, tokval, sp, ep, k in tokens:
    print toknum,tokval,sp,ep,k


