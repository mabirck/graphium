#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo, logging
from Helper import Helper
class Logger:
        
    _instance   = None
    _helper     = Helper()
    
    logging     = None
    
    def __init__(self,level='INFO'):
        self.logging            = logging
        self.logging.basicConfig(filename='log/scissor.log',level=logging.DEBUG)
        self.logging.Formatter(fmt='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        self.level              = level
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
    def error(self,message):
        self.logging.error(self._helper.getTimeNow()+" "+message)
        
    def critical(self,message):
        self.logging.critical(self._helper.getTimeNow()+" "+message)
        
    def warning(self,message):
        self.logging.warning(self._helper.getTimeNow()+" "+message)
        
    def info(self,message):
        self.logging.info(self._helper.getTimeNow()+" "+message)

    def debug(self,message):
        self.logging.debug(self._helper.getTimeNow()+" "+message)