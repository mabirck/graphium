#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob, os, json, sys
class LossAndAcc:
    
    folder_path = None
    files       = None
    file_path   = None
    
    def __init__(self,file=None):
        
        self.file_path      = file
        self.folder_path    = "../data/"
        self.files          = [] 
        
    def start(self):
        
        
        if self.file_path == None:
            
            os.chdir(self.folder_path)
            file_number = 0
            
            for file in glob.glob("*.json"):
                self.files.append(file)
                print "File", file_number, ":", file
                file_number+=1
                
            position = int(raw_input("Enter number: number "))
            with open(self.folder_path+self.files[position]) as file:
                self._proccess_file(file)    
        else:
            with open(self.file_path, 'r') as file:
                self._proccess_file(file)
                
    def _proccess_file(self,file):
        data = json.load(file)
        file_name = os.path.basename(file.name)
        file_name = file_name.split('.')[0]
        with open(self.folder_path+file_name+".csv",'w') as file_out:
            loss = "loss;"
            for value in data['loss']:
                loss += str(value).replace(".",",")+";"
            file_out.write(loss+os.linesep)
            acc = "acc;"
            for value in data['acc']:
                acc += str(value).replace(".",",")+";"
            file_out.write(acc+os.linesep)
        
if __name__ == '__main__':
    
    commands = sys.argv[1:len(sys.argv)]
    for i in range(len(commands)):
        commands[i] = commands[i].lower()
        
    lossAndAcc = LossAndAcc(commands[0])
    lossAndAcc.start()