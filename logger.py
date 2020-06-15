import logging

class myLogger:
    def __init__(self,*args,**kargs):
        self.__dict__.update(**kargs)
        self.logger=logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.sh=logging.StreamHandler()
        self.sh.setLevel(logging.DEBUG)
        self.sh.setFormatter(logging.Formatter('%(asctime)s - (%(threadName)-9s) - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.sh)

    def debug(self, *msg, **kwargs):
        self.logger.debug(' '.join(map(str, msg)), **kwargs)

    def info(self, *msg, **kwargs):
        self.logger.info(' '.join(map(str, msg)), **kwargs)

    def warning(self, *msg, **kwargs):
        self.logger.warning(' '.join(map(str, msg)), **kwargs)

    def error(self, *msg, **kwargs):
        self.logger.error(' '.join(map(str, msg)), **kwargs)

    def alert(self, *msg,  **kwargs):
        self.logger.critical(' '.join(map(str, msg)), **kwargs)

