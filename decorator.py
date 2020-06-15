from functools import wraps


def myDec1(func):
    def wrapperFunc(*args,**kwargs):
        print('I am on myDec1')
        print('Inside Wrapper   func:',func)
        print('Inside wrapper   args:',args)
        print('Inside wrapper   kwargs:',kwargs)
        print('Inside Wrapper   **kwargs:',**kwargs)
        print('Inside Wrapper   **kwargs:',func.__name__)
        print('func                 :',dir(func))
        clsbkp=func
        return func(*args,**kwargs)
    return wrapperFunc



def myDec(func):
    @wraps(func)
    def wrapperFunc(*args,**kwargs):
        print('I am on myDec')
        print('Inside Wrapper   func:',func)
        print('Inside wrapper   args:',args)
        print('Inside wrapper   kwargs:',kwargs)
        print('Inside Wrapper   **kwargs:',**kwargs)
        print('Inside Wrapper   **kwargs:',func.__name__)
        print('func                 :',dir(func))
        clsbkp=func
        return func(*args,**kwargs)
    return wrapperFunc



