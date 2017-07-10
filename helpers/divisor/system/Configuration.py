#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Configuration:
    
    _instance               = None
    # ficker configuration
    images_folder           = "data/"
    folder_test_name        = "test"
    folder_traning_name     = "trainning"
    test_size               = 0.4    
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance

	def __init__(self):
        
		print 'Config load' 