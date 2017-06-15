#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Configuration:
    
    _instance               = None
    
    folder_origin           = "../crawler/data/flickr/"#"data/origin/"
    folder_destiny          = "data/destiny/"
    
    # target
    target_window_porcent   = 0.8 # 0% to 100%. If 100 only one image with target will be create
    target_max_width        = 224
    target_max_height       = 224
    
    target_min_width        = 224
    target_min_height       = 224
    
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