#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Configuration:
    
    _instance           = None
    
    swarm_agent_number  = 1
    
    swarm_agent_names_API   = 'http://namey.muffinlabs.com/name.json?with_surname=true&frequency=all'
    swarm_agent_names       = ['Coralina Malaya','Abigail Johnson','Antonietta Marinese','Elisa Rogoff','Serafim Folkerts','Dulce Barrell']
    
    mongo_db            = "graphium"    # databse default
    mongo_host          = "localhost"   # host of mongodb
    mongo_port          = 27017         # port of mongodb
    
    colors              = ["#E91E63", "#9C27B0", "#F44336", "#673AB7", "#3F51B5", "#2196F3", "#00BCD4", "#009688", "#4CAF50", "#CDDC39", "#FF9800","#795548","#FF5722","#607D8B","#9E9E9E","#827717"]
    
    inf_positive        =  99999
    inf_negative        = -99999
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance

	def __init__(self):
		self.mongo_db            = "graphium"              # default file to training set
        self.mongo_host          = "localhost"           # default file with test set
        self.mongo_port          = 27017
        