'''
Created on 3 Dec 2013

@author: declan
'''
#print(list(filter(lambda x: x % 3 == 0, range(1,10))))

#problem 1
a = list(set(list(range(0, 1000, 3)) + list(range(0, 1000, 5))))
print(sum(a))

#problem 2
from itertools import islice

def fib(a=0, b=1):
    yield a
    while True:
        yield b
        a, b = b, a + b
fibonacci_numbers = list(islice(fib(), 20))
print(fibonacci_numbers)