import os, csv, sys

sys.path.append('..')
from system.Helper import Helper

class HotClasses:
    
    file_name               = None
    file_name_out           = None
    helper                  = None
    number_of_hot_classes   = 5
    _name_files             = []
    
    def __init__(self,file,number_of_classes=0):
        
        self.helper         = Helper()
        
        self.file_name      = file
        self.number_of_hot_classes = number_of_classes
        
        self.file_name_out  = "../data/"+self.helper.getSerialNow()+"_"+str(self.number_of_hot_classes)+"hot_by_image.csv"
        
        print 'HotClasses: File used     ', self.file_name
        print 'HotClasses: File generated', self.file_name_out
        
    def start(self):
        
        num_row         = 0
        num_coll        = 0
        array_values    = []
        array_position  = []
        file_out_csv    = open(self.file_name_out,'w')
        
        with open(self.file_name,'r') as csvfile:
            reader_csv = csv.reader(csvfile,delimiter=';')
            # for each row we create a array the number of classes
            #   and possible best values 
            for indx, row in enumerate(reader_csv):
                self._name_files.append(row[0])
                array_values.append([0.0]*self.number_of_hot_classes)
                array_position.append([0]*self.number_of_hot_classes) 
        
        with open(self.file_name,'r') as csvfile:
            reader_csv = csv.reader(csvfile,delimiter=';')
            # for each row in file
            #   if row == header
            #       create the hearder with the name of classes
            #   else
            #       for each coll in row
            #           if the value is great the each values in array of row
            #               change the min position and value for corrent value
            for row in reader_csv:
                print 'HotClasses: Processing row',num_row
                if num_row == 0: 
                    the_header = ""
                    for colum in row:
                        if num_coll != 1001:
                            the_header += colum+";"
                        num_coll+=1
                    the_header += os.linesep
                    file_out_csv.write(the_header)
                else:
                    for collum in row:
                        if num_coll== 0:
                            None#array_values[num_coll][0]+= 0  
                        elif num_coll != 1001:
                            the_max_value = float(max(array_values[num_row]))
                            the_min_value = float(min(array_values[num_row]))
                            the_value = float(collum)
                            if the_value > the_min_value:
                                the_position = array_values[num_row].index(the_min_value)
                                array_values[num_row][the_position] = the_value
                                array_position[num_row][the_position] = num_coll
                        num_coll+=1
                num_row += 1
                num_coll = 0
                
        num_row = 0
        # for each classe
        #   if position is on positions
        #       value is one (hot)
        #   else
        #       value is zero 
        for num, positions in enumerate(array_position):
            the_values = ""
            the_values+= self._name_files[num]
            #print 'Positions',positions
            #print 'Values   ',array_values[num]
            if num != 0:
                for i in range(1001):
                    if i in positions:
                        the_values  += "1;"
                    else:
                        the_values  += "0;"            
                the_values += os.linesep
                file_out_csv.write(the_values)
                
        file_out_csv.close()
        
        print 'HotClasses: Finish!'
        
    def getFilePath(self):
        return self.file_name_out
    
if __name__ == "__main__":
    
    commands = sys.argv[1:len(sys.argv)]
    for i in range(len(commands)):
        commands[i] = commands[i].lower()
    
    if '-f' in commands:
        t_index = commands.index('-f')
        file_name = commands[t_index+1]
    num_class= 5
    if '-c' in commands:
        t_index = commands.index('-c')
        num_class = int(commands[t_index+1])
    
    hotClasses = HotClasses(file_name,num_class)
    hotClasses.start()