import os, sys

from HotClasses import HotClasses
from HotHistogram import HotHistogram

if __name__ == "__main__":
    
    commands = sys.argv[1:len(sys.argv)]
    for i in range(len(commands)):
        commands[i] = commands[i].lower()
    
    if '-f' in commands:
        t_index = commands.index('-f')
        file_name = commands[t_index+1]
    
    oneClasses = HotClasses(file_name,1)
    oneClasses.start()
    oneHistogram = HotHistogram(oneClasses.getFilePath(),1)
    oneHistogram.start()
    