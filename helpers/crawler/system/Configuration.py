#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Configuration:
    
    _instance               = None
    # ficker configuration
    flickr_public_key       = "a6550e66205320e583d9bfb13a4b8634"
    flickr_private_key      = "3df7fce568942ae1"    
    
    flickr_tags             = "graffiti"            # Choose one or more tags split by comma
    flickr_folder           = "data/flickr/"        # folder of files
    flickr_size             = "larger"               # Choose ths width size => "larger", "medium" and "small". Default larger
    flickr_size_minimum     = 240                   # minimum px on width image
    flickr_size_maximum     = 1800                  # maximum px on width image
    
    safe_mode               = True          # Protect to require only 3600 per hour
    
    # MongoDB
    mongo_db                = "graphium"    # databse default
    mongo_host              = "localhost"   # host of mongodb
    mongo_port              = 27017         # port of mongodb
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance

	def __init__(self):
        
		print 'Config load' 