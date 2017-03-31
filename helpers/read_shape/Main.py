# Import the necessary modules

from Reader import Reader

if __name__ == "__main__":
    reader = Reader()
    reader.osmToMongoDB()
    
    