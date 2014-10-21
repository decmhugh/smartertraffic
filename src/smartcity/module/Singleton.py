'''
Created on 13 Jun 2014

@author: declan
'''
class Singleton(object):
    _instance = None
    cache = {}
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
if __name__ == '__main__':
    pass