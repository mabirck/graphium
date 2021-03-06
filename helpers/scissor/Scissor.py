#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, os, glob, traceback

from wand.image import Image
from wand.display import display

from system.Configuration import Configuration
from system.Logger import Logger

class Scissor:
    
    _config = None
    _logger = None
    _files  = []
    _tmp_dir= None
    
    def __init__(self,type_crawler='flickr'):
        self._config    = Configuration()
        self._files     = ['data/mona-lisa.jpg','data/neural-style.png']
        self._logger    = Logger()
        self._tmp_dir   = "/tmp/"
    def start(self):
        self._logger.info('Scissor: Start a new session')
        path = self._config.folder_origin
        total_files     = len(os.listdir(path))
        current_file    = 0
        for file in os.listdir(path):
            self._logger.info('Scissor: Image {1} from {0}'.format( total_files, current_file))
            file_name = path+file
            if os.path.isfile(os.path.join(path, file)) and file != ".DS_Store" and os.stat(file_name).st_size!=0:
                #print 'file path',file
                try:
                    image = Img(file_name)
                    image.cut_to_fit(self._config.target_max_width, self._config.target_max_height, self._config.target_window_porcent, self._config.target_min_width,self._config.target_min_height)
                    image.close()
                    current_file += 1
                except Exception as error:
                    print 'Error!'
                    print traceback.format_exc()
                    self._logger.error('Scissor: Something was wrong at image '+file_name+' :/')
            for magickfile in glob.iglob(os.path.join(self._tmp_dir, 'magick-*')):
                os.remove(magickfile)
                    
                
class Img:
    
    _config = None
    _logger = None
    
    original_image_url  = ""
    original_width      = 0
    original_height     = 0
    image_name          = ""
    image_url           = ""
    image               = None
    width               = 0
    height              = 0
    window_width        = 0
    window_height       = 0
    manipulated         = False
    
    def __init__(self,image_url=""):
        
        self._config    = Configuration()
        self._logger    = Logger()
        
        self.original_image_url = image_url
        self.image_url          = image_url
        
        self.image_name = self.original_image_url.split('/')
        self.image_name = self.image_name[len(self.image_name)-1]
        self.image_name = self.image_name.split('.')
        self.image_name = self.image_name[0]
        
        with Image(filename=self.original_image_url) as img:
            
            self.image          = img.clone()
            
            self.width          = int(img.size[0])
            self.height         = int(img.size[1])
            self.window_width   = int(img.size[0])
            self.window_height  = int(img.size[1])
            self.original_width = int(img.size[0])
            self.original_height= int(img.size[1])
            
            #print 'Image ',self.original_image_url,' size: ',self.width,'x',self.height

    def cut_to_fit(self,max_width=None,max_height=None,rate=1.0,min_width=None,min_height=None):
        
        new_width   = 0
        new_height  = 0
        need_cut    = False
        need_rate   = False
    
        # First cut the windows based on rate
        if rate < 1.0:
            self.window_width   = int(self.width*rate)
            self.window_height  = int(self.height*rate)
            self.width          = self.window_width
            self.height         = self.window_height
            self.image.crop(width=self.window_width, height=self.window_height, gravity='center')
            #print 'Cut and rate',self.width,'x',self.height

        # Calculate if the width is greater than max width value
        if max_width != None and self.width > max_width:
            # cut the width first
            new_width           = max_width
            new_height          = int(math.ceil((self.height*max_width)/self.width))
            if new_height >= max_height:
                need_cut            = True
                self.manipulated    = True
                self.width          = new_width
                self.height         = new_height
                #print 'Need cut by max_width',new_width,'x',new_height

        # Calculate if the width is greater than max width value
        if max_height != None and self.height > max_height:
        #   # cut the height if necessary
            new_height          = max_height
            new_width           = int(math.ceil((self.width*max_height)/self.height))
            if new_width >= max_width:
                need_cut            = True
                self.manipulated    = True
                self.width          = new_width
                self.height         = new_height
                #print 'Need cut by max_height',new_width,'x',new_height

        # Save the file
        if need_cut:
            self.image.resize(self.width,self.height)
            #print 'Need resize ',self.width,'x',self.height

        self.image.crop(width=max_width, height=max_height, gravity='center')
        if need_cut or need_rate:
            #self._logger.info('Scissor: new image {0}-{1}x{2}_resized.{3}'.format( self.image_name, self.image.width, self.image.height, self.image.format.lower()))
            self.image.save(filename='{0}{1}-{2}x{3}_resized.{4}'.format(self._config.folder_destiny, self.image_name, self.image.width, self.image.height, self.image.format.lower()))
        elif max_height != None and max_width != None and max_height >= self.height and max_width >= self.width:
            #self._logger.info('Scissor: new image {0}-{1}x{2}_original.{3}'.format( self.image_name, self.image.width, self.image.height, self.image.format.lower()))
            self.image.save(filename='{0}{1}-{2}x{3}_original.{4}'.format(self._config.folder_destiny, self.image_name, self.image.width, self.image.height, self.image.format.lower()))
        else:
            self._logger.info('Scissor: not create new image {0}-{1}x{2}.{3} on repository'.format( self.image_name, self.image.width, self.image.height, self.image.format.lower()))
        
    def close(self):
        self.image.close()
        self._config = None
        self._logger = None
        
    