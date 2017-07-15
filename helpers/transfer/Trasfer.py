#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob, os, random
from shutil import copyfile

class Transfer:
    
    images_folder   = None
    images_destity  = None
    number_of_images= None
    selection_way   = None
    
    def __init__(self, images_folder='data/source', images_destity='data/destity', number_of_images=10, selection_way='random',copy=True):
        self.images_folder      = images_folder
        self.images_destity     = images_destity
        self.number_of_images   = number_of_images
        self.selection_way      = selection_way
        self.copy_way           = copy
        
    def execute(self):
        moved = 0
        if not os.path.exists(self.images_folder):
            print 'Source',self.images_folder,'not exist!'
            return False
        
        if not os.path.exists(self.images_destity):
            print 'Destity',self.images_destity,'was created'
            os.makedirs(self.images_destity)
        
        #os.chdir(self.images_folder)
        files_to_transfer = glob.glob(self.images_folder+"*.*")
        
        if self.selection_way == 'random':
            random.shuffle(files_to_transfer)
            
        files_names = []
        for file in files_to_transfer:
            files_names.append(file.split("/")[-1:][0])
        
        for file_name in files_names:
            if os.path.isfile(os.path.join(self.images_folder,file_name)) and file_name != ".DS_Store" and os.stat(self.images_folder+file_name).st_size!=0:
                if moved < self.number_of_images:
                    print 'file ',moved, 'name', file_name
                    if self.copy_way:
                        copyfile(self.images_folder+file_name, self.images_destity+file_name)
                    else:
                        shutil.move(self.images_folder+file_name, self.images_destity+file_name)
                    moved+=1
if __name__ == "__main__":
            
    transfers   = []
    transfers.append(Transfer('/home/glauco/data/graffiti_cropped/', '/home/glauco/data/ImageNetGraffiti/n06596364/', 25000, 'random', True))
    transfers.append(Transfer('/home/glauco/data/street_cropped/', '/home/glauco/data/ImageNetGraffiti/n01843065/', 25000, 'random', True)) 
    
    for transfer in transfers:
        transfer.execute()