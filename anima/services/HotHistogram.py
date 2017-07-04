import os, csv, sys

from system.Helper import Helper

class HotHistogram:
    
    file_name               = None
    file_name_out           = None
    helper                  = None
    number_of_hot_classes   = 0
    
    def __init__(self,file,number_of_classes=0):
        
        self.helper                 = Helper()
        
        self.file_name              = file
        self.number_of_hot_classes  = number_of_classes
        
        self.file_name_out          = "../data/"+self.helper.getSerialNow()+"_"+str(self.number_of_hot_classes)+"hot_histogram.csv"
        
        print 'HotHistogram: File          ', self.file_name
        print 'HotHistogran: File generated', self.file_name_out
        
    def start(self):
        
        num_row = 0
        num_coll= 0
        array_values = []
        file_out_csv       = open(self.file_name_out,'w')
        
        with open(self.file_name,'r') as csvfile:
            reader_csv = csv.reader(csvfile,delimiter=';')
            for row in reader_csv:
                print 'HotHistogram: Processing row',num_row
                if num_row == 0:
                    the_header = ""
                    for colum in row:
                        if num_coll != 1001:
                            the_header += colum+";"
                            array_values.append(0)
                        num_coll+=1
                    the_header += os.linesep
                    file_out_csv.write(the_header)
                    
                else:
                    for collum in row:
                        if num_coll== 0:
                            array_values[num_coll] = row[0]  
                        elif num_coll != 1001:
                            array_values[num_coll]  += int(collum)
                        num_coll+=1
                num_row += 1
                num_coll = 0
        the_values = ""
        for value in array_values:
            the_values += str(value)+";"
        the_values += os.linesep
        file_out_csv.write(the_values)
        file_out_csv.close()
        print 'HotHistogram: Finish!'

if __name__ == "__main__":
    
    commands = sys.argv[1:len(sys.argv)]
    for i in range(len(commands)):
        commands[i] = commands[i].lower()
    
    if '-f' in commands:
        t_index = commands.index('-f')
        file_name = commands[t_index+1]
        
    hotHistogram = hotHistogram(file_name)
    hotHistogram.start()