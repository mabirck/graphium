#!/usr/bin/env python
# -*- coding: utf-8 -*-
from system.Mongo import *

class Configuration:
    
    _instance           = None
    _mongo              = None
    
    swarm_agent_number      = 3
    swarm_agent_names_API   = "http://namey.muffinlabs.com/name.json?with_surname=true&frequency=all"
    swarm_agent_names       = ['Coralina Malaya','Abigail Johnson','Antonietta Marinese','Elisa Rogoff','Serafim Folkerts','Dulce Barrell']
    swarm_agent_colors  = ["#E91E63", "#9C27B0", "#F44336", "#673AB7", "#3F51B5", "#2196F3", "#00BCD4", "#009688", "#4CAF50", "#CDDC39", "#FF9800","#795548","#FF5722","#607D8B","#9E9E9E","#827717"]
    
    swarm_seconds_to_check_agents  = 3
    
    mongo_db            = "graphium"  
    mongo_host          = "localhost"
    mongo_port          = 27017
    
    inf_positive        =  99999
    inf_negative        = -99999
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            try:
                self._mongo = Mongo()
            except:
                print 'Error at connect on mongoDB'
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # The system start with default information
    #   but always wil try to get information from database
    def __init__(self):
        
        if self._mongo != None:
            if self._mongo.getConfiguration() == None:
                self._mongo.insertConfiguration()
            else:
                conf_from_db = self._mongo.getConfiguration()
                self.swarm_agent_number = conf_from_db.swarm_agent_number
                self.swarm_agent_names_API = conf_from_db.swarm_agent_names_API
                self.swarm_agent_names = conf_from_db.swarm_agent_names
                self.colors = conf_from_db.colors
                self.inf_positive = conf_from_db.inf_positive
                self.inf_negative = conf_from_db.inf_negative