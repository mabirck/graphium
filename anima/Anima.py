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
    
    _total_images           = None
    _total_image_session    = None
    _total_sessions         = None
    _current_file           = None
    
    _file_onehot_csv        = None
    _file_output_csv        = None
    
    def __init__(self):
        
        self._logger  = Logger()
        self._config  = Configuration()
        
        self._logger.info('Anima: init the anima...')
        
        self._images        = []
        self._images_session= []
        self._images_names  = []
        
        self._path          = self._config.folder_origin
        
        self._current_file          = 0
        self._total_image_session   = 0
        self._total_sessions        = 0
        
        self._file_output_csv       = open(self._config.output_csv_file,'w')
        self._file_onehot_csv       = open(self._config.output_onehot_csv_file,'w')
        
    def start(self):
        
        self._logger.info('Anima: Starting executation')
        self._session   = tf.Session()
        self._imgs      = tf.placeholder(tf.float32, [None, 224, 224, 3])
        self._vgg       = VGG16(self._imgs, self._config.vgg16_weights_path, self._session)

        self._total_files     = len(os.listdir(self._path))
        
        # Write the header on files output
        the_header = "Image Name;"
        for class_name in class_names:
            the_header += class_name+";"
        the_header+= os.linesep
        self._file_output_csv.write(the_header)
        self._file_onehot_csv.write(the_header)
        
        self._logger.info('Anima: Read and send files to session')
        
        # each file on directory
        #   if file is not empty or is image
        #       adding image to list of images
        #       adding image to image session list
        #   if number of images is igual a batch size
        #       execute Session function
        # if list of images is different of 0
        #   execute Session function
        for file in os.listdir(self._path):
                
            file_name = self._path+file
            if os.path.isfile(os.path.join(self._path, file)) and file != ".DS_Store" and os.stat(file_name).st_size!=0:
                img1 = imread(file_name, mode='RGB')
                img1 = imresize(img1, (224, 224))
                self._logger.info('Anima: Appending image {0} {2} from {1}'.format( file, self._total_files, self._current_file))
                self._images_session.append(img1)
                self._images_names.append(file)
                self._total_image_session   += 1
            else:
                self._logger.info("Anima: Can't apppend image {0} to session".format(file))
            self._current_file          += 1
            
            
            if self._total_image_session!= 0 and self._total_image_session % self._config.session_batch_size == 0:
                self.executeSession()
                
        if self._total_image_session != 0:
            self.executeSession()
                
        self._file_onehot_csv.close()
        self._file_output_csv.close()
    
    def executeSession(self):
        self._logger.info('Anima: Start sessing {0} with {1} images'.format(self._total_sessions, len(self._images_session)))
        
        # Start a tf session from list of imagens session
        #   for each probability in probabilities
        #       set the probability on file
        #       set the hot value on file
        
        probabilities_by_image  = self._session.run(self._vgg.probs, feed_dict={self._vgg.imgs: self._images_session})

        img_position    = 0
        hot_position    = 0
        column_position = 0
        hot_value       = 0
        
        self._logger.info('Anima: Adding probabilities...')
        for probabilities in probabilities_by_image:

            # register the probabilities on output
            row_output    = self._images_names[(self._total_sessions * self._config.session_batch_size)+img_position-1]+";"
            for probability in probabilities:
                row_output += str(probability)+";"
            self._file_output_csv.write(row_output+os.linesep)

            # register the one hot value
            hot_position    = 0
            hot_value       = -99999
            column_position = 0
            for probability in probabilities:
                if hot_value <= probability:
                    hot_value       = probability
                    hot_position    = column_position
                column_position+=1

            # create the file with the one hot
            row_onehot  = self._images_names[(self._total_sessions * self._config.session_batch_size)+img_position-1]+";"
            for i in range(len(probabilities)):
                if i == hot_position:
                    row_onehot += "1;"
                else:
                    row_onehot += "0;"
            self._file_onehot_csv.write(row_onehot+os.linesep)

            # next image row processed
            img_position+=1

        self._logger.info('Anima: End the session executation')
        self._total_sessions += 1
        self._total_image_session   =0
        self._images_session = []
        