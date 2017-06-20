import os
import tensorflow as tf

from VGG16 import VGG16 
from Imagenet_classes import class_names

from system.Configuration import Configuration

if __name__ == '__main__':
    
    config  = Configuration()
    
    sess    = tf.Session()
    imgs    = tf.placeholder(tf.float32, [None, 224, 224, 3])
    vgg     = VGG16(imgs, config.vgg16_weights_path, sess)
    
    images = []
    images_names = []
    path = config.folder_origin
    total_files     = len(os.listdir(path))
    current_file    = 0
    for file in os.listdir(path):
        
        file_name = path+file
        if os.path.isfile(os.path.join(path, file)) and file != ".DS_Store" and os.stat(file_name).st_size!=0:
            img1 = imread(file_name, mode='RGB')
            img1 = imresize(img1, (224, 224))
            self._logger.info('Anima: Appending image {0} {2} from {1}'.format( file, total_files, current_file))
            images.append(img1)
            images_names.append(file)
        else
            self._logger.info('Anima: Cant apppend image {0}'.format(file))
        current_file += 1
        
    
    self._logger.info('Anima: Start a session...')
    
    probabilities_by_image  = sess.run(vgg.probs, feed_dict={vgg.imgs: images})
    
    file_output_csv         = open(config.output_csv_file,'w')
    
    self._logger.info('Anima: Write file from output...')
    the_header = "Image Name;"
    for class_name in class_names:
        the_header += class_name+";"
        
    file_output_csv.write(the_header)
    
    position = 0
    for probabilities in probabilities_by_image:
        row = images_names[position]+";"
        for probalility from probabilities:
            row += probalility+";"
        position+=1
        file_output_csv.write(row)
    
    file_output_csv.close()
    #preds = (np.argsort(probabilities_by_image)[::-1])[0:5]
    #for p in preds:
    #    print class_names[p], prob[p]
