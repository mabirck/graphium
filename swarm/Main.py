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
        
    if '-i' in commands:
        t_index = commands.index('-i')
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
        
    if '-a' in commands:
        t_index = int(commands.index('-a'))
        swarm_num_agent = int(commands[t_index+1])
    else:
        swarm_num_agent = config.swarm_agent_number
        
    if '-c' in commands:
        t_index = commands.index('-c')
        swarm_city = commands[t_index+1]
    else:
        swarm_city = config.city_id
        
    if '-t' in commands:
        t_index = commands.index('-t')
        swarm_turns = int(commands[t_index+1])
    else:
        swarm_turns = config.swarm_seconds_to_check_agents
        
    if '-y' in commands:
        t_index = commands.index('-y')
        swarm_cycles = int(commands[t_index+1])
    else:
        swarm_cycles = config.swarm_agent_cycles_number
        
    host = socket.gethostbyname(socket.gethostname())
    
    if mongo.getSwarmByIdentifier(swarm_identifier) == None:
        mongo.insertSwarm(swarm_identifier, swarm_num_agent, user_email, swarm_name, host, swarm_turns, swarm_cycles, swarm_city)
    
    swarm = Swarm(swarm_identifier)
    swarm.start()
    
    
    
     
    