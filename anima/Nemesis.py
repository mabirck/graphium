from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from keras.utils import np_utils
from keras.optimizers import SGD

class Nemesis:
    _base_model = None
    _x          = None
    _predictions= None
    
    _samples_for_epoch  = 128
    _number_of_epoch    = 150
    _number_of_classes  = 1000
    
    _callback_history   = LossHistory()
    
    
    def __init__(self):
        # create the base pre-trained model
        self._base_model = VGG16(weights='imagenet', include_top=True)
        
        self._callback_history = LossHistory()
        
        self.x = self._base_model.output
        
        self.print_layers()

    def start(self):
        
        # frozen the layout after the last
        for layer in self.base_model.layers[:self._model.layers.length-2]:
            layer.trainable = False
            
        # traing the last layer
        for layer in self.base_model.layers[self._model.layers.length-2:]:
            layer.trainable = True

        self.model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')
        
        self.model.fit_generator(Generator().getDatemageGenerator(), self._number_of_classes, self._number_of_epoch, verbose=2, show_accuracy=True, callbacks=[self._callback_history], validation_data=None, class_weight=None, nb_worker=1)

    
    def print_layers(self):
        for i, layer in enumerate(self._base_model.layers):
            print(i, layer.name, layer.get_config())
            
        
# fine tune
#   https://gist.github.com/fchollet/7eb39b44eb9e16e59632d25fb3119975
class Generator:

    _imageDateImage         = None
    _validation_generator   = None
    _predictions            = None
    
    _taget_size     = 244
    _batch_size     = 128
    
    def __init(self):
        
        self._imageDateimage        = image.ImageDataGenerator(rescale=1./255,shuffle=False).flow_from_directory('/path/', target_size=(self._taget_size, self._taget_size),batch_size=self.batch_size,class_mode='categorical')
        
        self.predictions = self._base_model.predict_generator(self._imageDateimage, len(self._imageDateimage.filenames))
       
    def getDatemageGenerator():
        self._imageDateimage
    
# callback history
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
