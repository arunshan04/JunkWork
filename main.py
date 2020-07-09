import threading
import time
import concurrent.futures as cf
import logging
import time
import random

logger_format = '%(asctime)s:%(threadName)s:%(message)s'
logging.basicConfig(format=logger_format, level=logging.INFO, datefmt="%H:%M:%S")



class emden(object):
    inst=None
    def __new__(cls,*args,**kwargs):
        if not cls.inst:
            cls.inst=super().__new__(cls)
        return cls.inst

    def __init__(self,*args,**kwargs):
        self.__thread__=[]
        print('inside Init....:',self,'Args:',args,'Kwargs:',kwargs)
        self.__dict__.update(**kwargs)
        self.args=args
        self.event=threading.Event()

    def wrapper(self,*args,**kwargs):
        while not self.event.isSet():
            time.sleep(10)
            print('Inside Wrapper...:',self,'Args:',args,'Kwargs:',kwargs)
        print('Threads are Stoped Now....',len(self.__thread__))

    def Threadedwrapper(self,*args,**kwargs):
        logging.info('Recieved...')
        #while not self.event.isSet():
        sl=random.randint(0,20)
        logging.info('Sleeping...'+str(sl))
        time.sleep(sl)
        print('Inside Wrapper...:',self,'Args:',args,'Kwargs:',kwargs)
        print('Threads are Stoped Now....',len(self.__thread__))

    def startT(self):
        self.__thread__=[]
        with cf.ThreadPoolExecutor(max_workers=2) as executor:
            future_to_mapping = {executor.submit(self.Threadedwrapper,i ): i for i in self.Dir}
            print(future_to_mapping)
            for future in cf.as_completed(future_to_mapping):
                logging.info(f"{future.result()} Done")

    def start(self):
        self.__thread__=[]
        for j in self.Dir:
            thrd=threading.Thread(target=self.wrapper,args=[j],name=j)
            thrd.start()
            self.__thread__.append(thrd)
        return self 

    def stop(self):
        return s.event.set()
        #return [s.join() for s in s.__thread__]

    @property
    def totalRunning(self):
        return '{} Running'.format(len(list(filter(lambda x:x.isAlive(),self.__thread__))))







