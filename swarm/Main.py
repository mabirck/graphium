#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from system.Configuration import *
from system.Mongo import *
from API import API
from Swarm import *

if __name__ == "__main__":
    
    config  = Configuration()
    mongo   = Mongo()
    api     = API()
    swarm   = None
    
    # read the argv to get commands
    commands = sys.argv[1:len(sys.argv)]
    for i in range(len(commands)):
        commands[i] = commands[i].lower()
        
    if '-a' in commands:
        t_index = commands.index('-a')
        agent_number = commands[t_index+1]
    else:
        agent_number = None
        
    if '-r' in commands:
        db_reset = True
    else:
        db_reset = False
    
    swarm = Swarm(agent_number,db_reset)
    #try:
        
    #except Exception,e:
    #    print 'Failed to upload to ftp: '+ str(e)
    #    swarm.closeSwarm()
        
    swarm.closeSwarm()
    
    
     
    