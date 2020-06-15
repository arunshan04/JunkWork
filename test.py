import os
import re
import logging
import functools
import time
import datetime
import time
import platform
import collections
from concurrent.futures import ProcessPoolExecutor

_sL=collections.defaultdict(int)
host=platform.uname()[1].split('.')[0]

def multiprocessing(func, args, workers):
    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)

def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler(r"/tmp/test.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger

logger = create_logger()
# exception_decor.py



def exception(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
            
            # re-raise the exception
          #  raise
        return wrapper
    return decorator

@exception(logger)
def digger(path,pattern,depth=None):
    if os.path.isfile(path) and not os.path.islink(path):
        return ([(path,os.stat(path))],[])[pattern.search(path)==None]
        #if pattern.search(path):
        #    return [(path,os.stat(path))]
        #else:
        #    return []
    elif os.path.isdir(path):
        if not path.endswith('/'):
            path=path+'/'
        l=[]
        if depth is None: depth=-1;
        if depth != 0:
            try :
                for j in os.listdir(path): 
                    l=l+digger(path+j,pattern,depth-1)
            except OSError: 
                pass
        return l
    else:return []

def Watcher(path,sleep=60,pattern='.*',func=None,watcher=True,level=None):
    reg=re.compile(pattern)
    _bF=dict(digger(path,reg,level))
    while 1:
        time.sleep(sleep)
        _aF=dict(digger(path,reg,level))
        _a1=list(set(_aF.keys())-set(_bF.keys()))
        _a2=list(set(_bF.keys())-set(_aF.keys()))
        _a3=list(filter(lambda x:x and _aF.get(x).st_size > _bF.get(x).st_size,list(set(_bF.keys()).intersection(set(_aF.keys())))))
        _a4=list(filter(lambda x:x and _aF.get(x).st_size < _bF.get(x).st_size,list(set(_bF.keys()).intersection(set(_aF.keys())))))
        _a5=list(filter(lambda x:x and _aF.get(x).st_mtime >  _bF.get(x).st_mtime,list(set(_bF.keys()).intersection(set(_aF.keys())))))
        _a6=list(filter(lambda x:x and _aF.get(x).st_mtime < _bF.get(x).st_mtime,list(set(_bF.keys()).intersection(set(_aF.keys())))))
        #print(_a1,_a2,_a3,_a4,_a5,_a6)
        events=list(map(lambda x:(dict([('EventTime',datetime.datetime.now().strftime('%s')),('EventHost',host),('EventId','Added'),('File',x),('Size',_aF[x].st_size),('Updated',_aF[x].st_mtime)])),_a1))+list(map(lambda x:(dict([('EventTime',datetime.datetime.now().strftime('%s')),('EventHost',host),('EventId','Deleted'),('File',x),('Size',_bF[x].st_size),('Updated',_bF[x].st_mtime)])),_a2))+list(map(lambda x:(dict([('EventTime',datetime.datetime.now().strftime('%s')),('EventHost',host),('EventId','Updated'),('File',x),('Size',_aF[x].st_size),('Updated',_aF[x].st_mtime)])),dict.fromkeys(_a3+_a4+_a5+_a6)))
        if events:print(events)
        _bF=_aF



def Blaster(path,sleep=60,pattern='.*',func=None,watcher=True,level=None):
    reg=re.compile(pattern)
    _bF=dict(digger(path,reg,level))
    while 1:
        time.sleep(sleep)
        _aF=dict(digger(path,reg,level))
        _a1=list(set(_aF.keys())-set(_bF.keys()))   ##Added
        _a2=list(set(_bF.keys())-set(_aF.keys()))   ##Deleted
        _a3=list(filter(lambda x:x and _aF.get(x).st_size > _bF.get(x).st_size,list(set(_bF.keys()).intersection(set(_aF.keys())))))                     ### Modified
        _a4=list(filter(lambda x:x and _aF.get(x).st_size < _bF.get(x).st_size,list(set(_bF.keys()).intersection(set(_aF.keys())))))                     ### Size Reduced
        _a5=list(filter(lambda x:x and _aF.get(x).st_mtime >  _bF.get(x).st_mtime,list(set(_bF.keys()).intersection(set(_aF.keys())))))                  ### Modified Time Increased
        _a6=list(filter(lambda x:x and _aF.get(x).st_mtime < _bF.get(x).st_mtime,list(set(_bF.keys()).intersection(set(_aF.keys())))))                  ### Modified Time decreased
        _bF=_aF
        for i in _a2+_a4+_a6+list(set(_a5)-set(_a3)):
            if i in _sL.keys():
                del _sL[i]
        for i in _a3+_a1:
            if i not in _sL.keys():
                _sL[i]=0
        for file in set(_a3+_a4+_a5+_a6):
            with open(file,'r') as file_:
                file_.seek(_sL[file])
                try:
                    lines=file_.readlines()
                    _sL[file]=file_.tell()
                    #func(lines)
                    multiprocessing(func=func,args=lines,workers=len(lines))
                except:pass
