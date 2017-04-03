#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo, logging

from Mongo import Mongo

class Logger:
        
    _instance   = None
    
    _mongo      = None
    _level      = None
    _session    = None
    logging     = None

    def __init__(self,swarm_session,level='INFO'):
        
        self._mongo             = Mongo()
        self.logging            = logging
        self.logging.basicConfig(filename='log/graphium_swarm.log',level=logging.DEBUG)
        self.level              = level
        self.swarm_session      = swarm_session
            
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
    def error(self,message):
        self.__message(message,"ERROR");
        self.logging.error(message)
        
    def critical(self,message):
        self.__message(message,"CRITICAL");
        self.logging.critical(message)
        
    def warning(self,message):
        self.__message(message,"WARNING");
        self.logging.warning(message)
        
    def info(self,message):
        self.__message(message,"INFO");
        self.logging.info(message)

    def debug(self,message):
        self.__message(message,"DEBUG");
        self.logging.debug(message)
        
    def __message(self,message="",level=None):
        if level == None:
            level = self.level   
        self._mongo.addLog(message,level,self.swarm_session)
        