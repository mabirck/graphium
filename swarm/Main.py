#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, socket

from system.Configuration import *
from system.Mongo import *
from system.Helper import *
from API import API
from Swarm import *

if __name__ == "__main__":
    
    config  = Configuration()
    mongo   = Mongo()
    helper  = Helper()
    api     = API()
    swarm   = None
    
    # read the argv to get commands
    commands = sys.argv[1:len(sys.argv)]
    for i in range(len(commands)):
        commands[i] = commands[i].lower()
        
    if '-s' in commands:
        t_index = commands.index('-s')
        swarm_identifier = commands[t_index+1]
    else:
        swarm_identifier = helper.getSerialSwarmNow()
        
    if '-u' in commands:
        t_index = commands.index('-u')
        user_email = commands[t_index+1]
    else:
        user_email = "admin@graphium.com"
        
    if '-n' in commands:
        t_index = commands.index('-n')
        swarm_name = commands[t_index+1]
    else:
        swarm_name = helper.getTimeNow()
        
    host = socket.gethostbyname(socket.gethostname())
    
    if mongo.getSwarmByIdentifier(swarm_identifier) == None:
        mongo.insertSwarm(swarm_identifier, config.swarm_agent_number, user_email, swarm_name, host)
    
    swarm = Swarm(swarm_identifier)
    swarm.start()
    
    
    
     
    