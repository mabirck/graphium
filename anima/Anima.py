import os
import tensorflow as tf

from scipy.misc import imread, imresize

from VGG16 import VGG16 
from Imagenet_classes import class_names
from system.Configuration import Configuration
from system.Logger import Logger


class Anima:
    
    _config     = None
    _logger     = None
    
    _session    = None
    _imgs       = None
    _images     = None
    _vgg        = None
    _path       = None
    
    _total_images   = None
    _current_file   = None
    
    def __init__(self):
        self._logger  = Logger()
        self._config  = Configuration()
        self._logger.info('Anima: init a session...')
        
        self._images        = []
        self._images_names  = []
        self._path          = self._config.folder_origin
        self._current_file  = 0
        
        
    def start(self):
        self._session   = tf.Session()
        self._imgs      = tf.placeholder(tf.float32, [None, 224, 224, 3])
        self._vgg       = VGG16(self._imgs, self._config.vgg16_weights_path, self._session)

        self._total_files     = len(os.listdir(self._path))
        
        
        for file in os.listdir(self._path):
        
            file_name = self._path+file
            if os.path.isfile(os.path.join(self._path, file)) and file != ".DS_Store" and os.stat(file_name).st_size!=0:
                img1 = imread(file_name, mode='RGB')
                img1 = imresize(img1, (224, 224))
                self._logger.info('Anima: Appending image {0} {2} from {1}'.format( file, self._total_files, self._current_file))
                self._images.append(img1)
                self._images_names.append(file)
            else:
                self._logger.info('Anima: Cant apppend image {0}'.format(file))
            self._current_file += 1
        

        probabilities_by_image  = self._session.run(self._vgg.probs, feed_dict={self._vgg.imgs: self._images})

        file_output_csv         = open(self._config.output_csv_file,'w')

        self._logger.info('Anima: Write file from output...')
        the_header = "Image Name;"
        for class_name in class_names:
            the_header += class_name+";"
        the_header+= os.linesep
        file_output_csv.write(the_header)

        position = 0
        for probabilities in probabilities_by_image:
            row = self._images_names[position]+";"
            for probalility in probabilities:
                row += str(probalility)+";"
            position+=1
            file_output_csv.write(row+os.linesep)

        file_output_csv.close()
        
        