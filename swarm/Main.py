#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

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
        session_identifier = commands[t_index+1]
    else:
        session_identifier = None
        
    if '-u' in commands:
        t_index = commands.index('-u')
        user_email = commands[t_index+1]
    else:
        user_email = "admin@graphium.com"
        
    if '-n' in commands:
        t_index = commands.index('-n')
        user_name = commands[t_index+1]
    else:
        user_name = helper.getTimeNow()
    
    swarm = Swarm(session_identifier,user_name,user_email)
    swarm.start()
    
    
    
     
    