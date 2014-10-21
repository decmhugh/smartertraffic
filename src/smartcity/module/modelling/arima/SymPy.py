'''
Created on 3 Dec 2013

@author: declan
'''
import os,gc,sys
from sympy import *

#init_printing()
#init_session()
x,t = symbols('X t')
print(latex(x - t))
