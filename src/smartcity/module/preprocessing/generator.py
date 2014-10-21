'''
Created on 3 Dec 2013

@author: declan
'''

def step(n):
    num = 0
    while num < n:
        yield num
        num += 1



s = step(10)

print(list(s))