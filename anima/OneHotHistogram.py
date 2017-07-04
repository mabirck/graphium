import os, csv, sys

from system.Helper import Helper

class oneHotHistogram:
    
    file_name       = None
    file_name_out   = None
    helper          = None
    
    def __init__(self,file):
        
        self.file_name      = file
        self.helper         = Helper()
        self.file_name_out  = "data/"+self.helper.getSerialNow()+"_onehot_histogram.csv"
        
        print 'file used ',self.file_name
        
    def start(self):
        
        num_row = 0
        num_coll= 0
        array_values = []
        file_out_csv       = open(self.file_name_out,'w')
        
        with open(self.file_name,'r') as csvfile:
            reader_csv = csv.reader(csvfile,delimiter=';')
            for row in reader_csv:
                print 'processing row',num_row
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
                            array_values[num_coll]+= 0  
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

if __name__ == "__main__":
    
    commands = sys.argv[1:len(sys.argv)]
    for i in range(len(commands)):
        commands[i] = commands[i].lower()
    
    if '-f' in commands:
        t_index = commands.index('-f')
        file_name = commands[t_index+1]
        
    oneHotHistogram = oneHotHistogram(file_name)
    oneHotHistogram.start()