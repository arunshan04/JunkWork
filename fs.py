from loggers import BaseLogger
import itertools
import re

import os
class FSMonitor:
    def __init__(self,*args,**kwargs):
        self.logger=BaseLogger(self.__class__.__name__)
        self.__dict__.update(**kwargs)
        if self.__dict__.get('pattern',True):self.__dict__['pattern']='.*'
        self.pattern=re.compile(self.pattern)
        self.logger.info('Initiated ....',self.path)
        self.module_name=self.__module__

    @property
    def exists(self):
        return os.path.exists(self.path)
    
    @property
    def isFile(self):
        return os.path.isfile(self.path)
    
    @property
    def isLink(self):
        return os.path.islink(self.path)
    
    @property
    def isDir(self):
        return os.path.isdir(self.path)
    
    def getFiles(self):
        if self.isDir:
            return [(path,self._stat(path)) for path in filter(self.pattern.findall,[path for path in itertools.chain(*[ [i+'/'+m for m in k] for i,_,k in os.walk(self.path)])])]
        else: return [(self.path,self._stat(self.path))]
   
    @staticmethod
    def _stat(file):
        try :
            s=os.stat(file,follow_symlinks=False)
            return s
        except OSError:
            pass




class Watcher(FSMonitor):
    def __init__(self,*args,**kwargs):
        self.__dict__.update(**kwargs)
        super().__init__(self)

    def getAllFiles(self):
        for j in self.getFiles():
            pass

    def __repr__(self):
        return '<{cls_bases}: {name}>'.format(cls_bases=', '.join(c.__name__ for c in self.__class__.__bases__),name=self.path)

class PermissionError:
    pass

s=Watcher(path='/tmp')

#s.__isFile__(),s.__isLink__(),s.__isDir__()
#[(path,os.stat(path,follow_symlinks=False)) for path in itertools.chain(*[ [i+'/'+m for m in k] for i,_,k in s.getFiles()])]
