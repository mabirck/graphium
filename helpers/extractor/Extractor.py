import glob, os, sys, urllib2
from subprocess import call

class Extractor:
    
    _files_imagenet = None
    _destiny        = None
    _transfers      = []
    def __init__(self):
        self._files_imagenet    = "/mnt/dataWD1/ulisses/ImageNet/"#"data/"#
        self._destiny           = "/mnt/dataWD1/glauco/ImageNet/"#"data/imagenet/"#
            
    def start(self):
        
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
            try:
                print 'Waiting Imagenet-API...'
                namesOnHTML = urllib2.urlopen("http://www.image-net.org/api/text/wordnet.synset.getwords?wnid="+synset,timeout=100)
                names       = namesOnHTML.read()
                names       = names.split("\n")
                names       = names[:len(names)-1]
                needGet     = False
            except Exception as inst:
                print 'Will try again... Wait'
        
        if not "Invalid url!" in names:
            namesToFolder = ""
            for name in names:
                namesToFolder+= name+","
            namesToFolder = namesToFolder[:len(namesToFolder)-1]
            return namesToFolder
        else:
            return False
                
if __name__ == "__main__":
            
    extractor = Extractor()
    extractor.start()
    
    