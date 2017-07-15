#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Helper import Helper

class Configuration:
    
    _instance               = None
    _helper                 = Helper()
    
    folder_origin           = "data/images/" #"../helpers/scissor/data/destiny/"#"data/images/"#
    output_folder           = "data/"
    vgg16_weights_path      = "data/vgg16_weights.npz"
    output_csv_file         = "data/"+_helper.getSerialNow()+"_output_anima.csv"
    output_weights_file     = "data/"+_helper.getSerialNow()+"_weights.h5"
    session_batch_size      = 128 # number of imagens at each session
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance
