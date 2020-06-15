import time
import threading
from logger import myLogger

class single(object):
    _inst=[]
    _active=0
    _passive=0
    @property
    def active(self):
        return self.__class__._active
    @property
    def passive(self):
        return self.__class__._passive
    @property
    def instance(self):
        return len(self.__class__._inst)

    def __new__(cls,*args,**kargs):
        if len(cls._inst)<5:
            cls._inst.append(super(single,cls).__new__(cls))
            cls._passive+=1
            return cls._inst[-1]
    
    def __init__(self,*args,**kargs):
        self.args=args
        self.__dict__.update(**kargs)
        self.logger=myLogger(name=self.Name)
        self._event=threading.Event()
        self._thread=threading.Thread(name=self.Name,target=self.target,args=(self.logger,self._event,args,kargs))
        self.logger.info('Insitace Initatilized ....',id(self))

    def __call__(self):
        self.__class__._active+=1
        return self.__exit__()

    def start(self):
        self._thread.start()

    def __exit__(self):
        self.__class__._passive-=1
    
    def __repr__(self):
        return self.Name


def testfunc(logger,event,*args,**kargs):
        logger.info('Function Called..............')
        logger.info('Arguments           : ',*args,**kargs)
        event.wait()
        logger.debug('Executing Functiions After Long await',event.isSet())


