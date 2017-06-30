#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Helper import Helper

class Configuration:
    
    _instance               = None
    _helper                 = Helper()
    
    folder_origin           = "../helpers/scissor/data/destiny/"#"data/images/"#
    vgg16_weights_path      = "data/vgg16_weights.npz"
    output_csv_file         = "data/"+_helper.getSerialNow()+"_out_putout_.csv"
    output_onehot_csv_file  = "data/"+_helper.getSerialNow()+"_out_onehot.csv"
    
    session_batch_size      = 256 # number of imagens at each session
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance