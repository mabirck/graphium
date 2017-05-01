import datetime

class Helper:
    _instance   = None
    
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Helper, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        None
    
    def getSerialNow(self):
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    def getTimeNow(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")