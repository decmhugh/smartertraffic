import functools

P = lambda x,z: x*z
T = lambda x: functools.reduce(P,range(1,x+1))
print(T(4))