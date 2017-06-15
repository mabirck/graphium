#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Configuration:
    
    _instance               = None
    
    folder_origin           = "../helpers/scissor/data/destiny/"
    vgg16_weights_path      = "data/vgg16_weights.npz"
    output_csv_file         = "data/out_put.csv"
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance