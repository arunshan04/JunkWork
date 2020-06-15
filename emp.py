class dept():
    dlist={}
    def __new__(cls,*args,**kwargs):
        print(cls,args,kwargs)
        if not cls.dlist.get(kwargs['id']):
            return object().__new__(cls)
        return cls.dlist[kargs['id']]

    def __init__(self,*args,**kwargs):
        if not self.dlist.get(kwargs['id']):
            self.__dict__.update(**kwargs)
            self.__class__.dlist[kwargs['id']]=self
            self.Department='MyDepartment'

class emp(dept):
    elist={}
    def __new__(cls,*args,**kwargs):
        if not cls.elist.get(kwargs['id']):
            #return super(emp,cls).__new__(cls)
            return object().__new__(cls)
        return cls.elist[kwargs['id']]

    def __init__(self,*args,**kwargs):
        print(kwargs)
        if not self.elist.get(kwargs['id']):
            dept.__init__(self,*args,**kwargs)
            self.__dict__.update(**kwargs)
            self.__class__.elist[kwargs['id']]=self
        print(hash(self))



