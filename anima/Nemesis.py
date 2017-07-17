#!/usr/bin/env python
# -*- coding: utf-8 -*-

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.models import Model
from keras.optimizers import SGD
from system.Configuration import Configuration
from system.Helper import Helper
from Callbacks import JSONMetrics

class Nemesis:
    
    _config             = None
    _base_model         = None
    
    _samples_for_epoch  = 128
    _number_of_epoch    = 150
    _number_of_classes  = 1000
    
    _callbacks          = []
    
    def __init__(self):
        # create the base pre-trained model
        self._config    = Configuration()
        
        self._base_model= VGG16(weights='imagenet', include_top=True)
        
        self._callbacks.append(JSONMetrics(self._base_model,2))
        
        self.x = self._base_model.output
        
        self.print_layers()

    def start(self):
        
        # frozen the layout after the last
        for layer in self._base_model.layers[:len(self._base_model.layers)-2]:
            layer.trainable = False
            
        # traing the last layer
        for layer in self._base_model.layers[len(self._base_model.layers)-2:]:
            layer.trainable = True

        self._base_model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])
        
        self._base_model.fit_generator(Generator().getDatemageGenerator(), self._number_of_classes, self._number_of_epoch, verbose=2, callbacks=self._callbacks, validation_data=None, class_weight=None)
       
        self._base_model.save_weights(self._config.output_weights_file)
    
    def print_layers(self):
        print self._base_model.summary()
        #for i, layer in enumerate(self._base_model.layers):
        #    print(i, layer.name, layer.get_config())
            
        
# fine tune
#   https://gist.github.com/fchollet/7eb39b44eb9e16e59632d25fb3119975
class Generator:

    _imageDateImage         = None
    
    _taget_size             = 224   # size of pic (w x h)
    _batch_size             = 128
    
    _path_directory         = "/home/glauco/data/ImageNetGraffiti/"
    _path_directory_classes = "../helpers/extractor/data/synset_words.txt"
    _path_classes_name      = []
    
    def __init__(self):
        
        with open(self._path_directory_classes) as file:
            lines = file.readlines()
            for line in lines:
                self._path_classes_name.append(line[:9])
        self._imageDateimage        = image.ImageDataGenerator(rescale=0).flow_from_directory(self._path_directory, target_size=(self._taget_size, self._taget_size), batch_size= self._batch_size, class_mode='categorical', shuffle=True,classes=self._path_classes_name)
        
    def getDatemageGenerator(self):
        return self._imageDateimage
    

if __name__ == '__main__':
        
    generator = Generator()