import glob, os, sys, urllib2, random
from subprocess import call

class Extractor:
    
    _files_imagenet = None
    _destiny        = None
    _transfers      = []
    def __init__(self):
        self._files_imagenet    = "/mnt/dataWD1/ulisses/ImageNet/"#"data/"
        self._destiny           = "/mnt/dataWD1/glauco/ImageNet/"#"data/imagenet/"
        self._transfers.append(Transfer('data/imagenet/honeycomb/','data/imagenet/honeycomb_2/',10,'random')) 
        #with file in op
       
    def start(self):
        self.untar()
        #self.transfers()
        
    def transfers(self):
        for transfer in self._transfers:
            transfer.execute()
            
    def untar(self):
        
        
        # check if destiny exists
        if not os.path.exists(self._destiny):
            os.makedirs(self._destiny)
        
        #for each .tar
        #   check if existe the folder with the name
        #   untar the content in folder
        for file_name in glob.glob(self._files_imagenet+"*.tar"):
            
            # get synset from tar file
            # create the name of directory from synset code
            file_tar            = file_name
            file_name           = file_name.split("/")
            file_name           = file_name[-1:][0]
            synset              = file_name.split(".")[0]
            
            print 'file tar', file_tar
            print 'synset  ', synset
            
            name_from_synset    = self.giveMeTheNames(synset)
            path_new_directory  = self._destiny+name_from_synset
            
            print 'destiny ', path_new_directory
            
            # check if directory exists
            # un tar each file 
            if not os.path.exists(path_new_directory):
                os.makedirs(path_new_directory)
            
            call(["tar", "xvf", file_tar, "-C", path_new_directory])    
        
        
        
    # send the exacty name used on imagent
    #   from synset sended
    def giveMeTheNames(self,synset):
        
        needGet = True
        names   = ""
        while needGet:
            
            # require names
            namesOnHTML = urllib2.urlopen("http://www.image-net.org/api/text/wordnet.synset.getwords?wnid="+synset,timeout=100)
            try:
                print 'Waiting Imagenet-API...'
                names       = namesOnHTML.read()
                names       = names.split("\n")
                names       = names[:len(names)-1]
                needGet     = False
            except e:
                print 'Will try again... Wait'
        
        if not "Invalid url!" in names:
            namesToFolder = ""
            for name in names:
                namesToFolder+= name+","
            namesToFolder = namesToFolder[:len(namesToFolder)-1]
            return namesToFolder
        else:
            return False
        
class Transfer:
    
    images_folder   = None
    images_destity  = None
    number_of_images= None
    selection_way   = None
    
    def __init__(self, images_folder='data/source', images_destity='data/destity', number_of_images=10, selection_way='random'):
        self.images_folder      = images_folder
        self.images_destity     = images_destity
        self.number_of_images   = number_of_images
        self.selection_way      = selection_way
        
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
                    os.rename(self.images_folder+file_name, self.images_destity+file_name)
                    moved+=1
        
if __name__ == "__main__":
            
    extractor = Extractor()
    extractor.start()
    
    