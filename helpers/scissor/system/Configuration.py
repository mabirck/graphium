#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Configuration:
    
    _instance               = None
    
    folder_origin           = "../crawler/data/flickr/"
    folder_destiny          = "data/destiny/"
    
    # windows Px size
    window_size_width       = 144
    window_size_heght       = 144
    
    # target
    target_window_porcent   = 0.8 # 0% to 100%. If 100 only one image with target will be create
    target_max_width        = 800
    target_max_height       = 500
    
    # MongoDB
    mongo_db                = "graphium"    # databse default
    mongo_host              = "localhost"   # host of mongodb
    mongo_port              = 27017         # port of mongodb
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init(self):
        if self.target_window_porcent > 1.0:
            self.target_window_porcent = self.target_window_porcent/float(100)
        print 'Config Load' 