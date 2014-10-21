
def wrap(pre, post):
    def decorate(func):
        def call(*args, **kwargs):
            pre(func, *args, **kwargs)
            result = func(*args, **kwargs)
            post(func, *args, **kwargs)
            return result
        return call
    return decorate

def trace_in(func, *args, **kwarg):
    print(kwarg)
    print("Entering function",  func.__name__)

def trace_out(func, *args, **kwargs):
    print("Leaving function", func.__name__)

@wrap(trace_in, trace_out)
def calc(x, *y , z=0):
    return x + sum(y) - z

print(calc(1,2,4,5,z=5))