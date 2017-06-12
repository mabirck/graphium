# Import the necessary modules
import time
from Scissor import Scissor
from system.Logger import Logger

if __name__ == "__main__":
    
    logger      = Logger()
    scissor     = Scissor()
    
    start       = time.time()
    scissor.start()
    end = time.time()
    
    elapsed = end - start
    logger.info('running at {0} seconds'.format( elapsed))
    print 'running at',elapsed,'seconds'