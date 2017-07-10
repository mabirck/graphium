from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.models import Model
from keras.optimizers import SGD
import keras.callbacks as callbacks

class Nemesis:
    _base_model = None
    _x          = None
    
    _samples_for_epoch  = 128
    _number_of_epoch    = 150
    _number_of_classes  = 1000
    
    _callback_history   = None
    
    def __init__(self):
        # create the base pre-trained model
        self._base_model = VGG16(weights='imagenet', include_top=True)
        
        self._callback_history = LossHistory()
        
        self.x = self._base_model.output
        
        self.print_layers()

    def start(self):
        
        # frozen the layout after the last
        for layer in self._base_model.layers[:len(self._base_model.layers)-2]:
            layer.trainable = False
            
        # traing the last layer
        for layer in self._base_model.layers[len(self._base_model.layers)-2:]:
            layer.trainable = True

        self._base_model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')
        
        self._base_model.fit_generator(Generator().getDatemageGenerator(), self._number_of_classes, self._number_of_epoch, verbose=2, show_accuracy=True, callbacks=[self._callback_history], validation_data=None, class_weight=None, nb_worker=1)

    
    def print_layers(self):

        for i, layer in enumerate(self._base_model.layers):
            print(i, layer.name, layer.get_config())
            
        
# fine tune
#   https://gist.github.com/fchollet/7eb39b44eb9e16e59632d25fb3119975
class Generator:

    _imageDateImage         = None
    
    _taget_size             = 244   # size of pic (w x h)
    _batch_size             = 128
    
    _path_directory         = "/mnt/dataWD1/glauco/ImageNet/"
    
    def __init__(self):
        
        self._imageDateimage        = image.ImageDataGenerator(rescale=0).flow_from_directory(self._path_directory, target_size=(self._taget_size, self._taget_size), batch_size= self._batch_size, class_mode='categorical', shuffle=False)
        
    def getDatemageGenerator(self):
        return self._imageDateimage
    
# callback history
class LossHistory(callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
