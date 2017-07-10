#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from wand.image import Image
from system import Configuration

class Divisor:
    
    _config         = None
    _path_image     = None
    _path_test      = None
    _path_training  = None
    
    def __init(self):
        self._config            = Configuration()
        
        self._path_image        = self._config.images_folder
        self._path_test         = self._config.images_folder+self._config.folder_test_name
        self._path_training     = self._config.images_folder+self._config.folder_traning_name
        
        if os.path.isFolder(os.path.join(path,))
        
    def start(self):
        
        for file in os.listdir(self._path_image):
            path_image_file = path_image+file
            if os.path.isFile(os.path.join(path_image,file)) and file != ".DS_Store" and os.stat(path_image_file).st_size!=0:
                try:
                    with Image(filename=filenamepath_image_file) as img:
                        image_to_save = img.clone()
                        image_to_save
                    
        