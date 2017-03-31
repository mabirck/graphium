#!/usr/bin/env python
# -*- coding: utf-8 -*-

from system.Configuration import *
from system.Mongo import *
from system.Helper import *
from Agent import *
import socket, datetime

class Swarm:
    
    _agents         = []
    _config         = None
    _swarm_config   = None
    _mongo          = None
    _helper         = None
    
    def __init__(self,agent_number = None,db_reset=False):
        
        self._swarm_config  = SwarmConfig()
        self._mongo         = Mongo()
        self._helper        = Helper()
        self.agentStoryDB()
        self.populationDB(db_reset)
        if agent_number != None:
            self._swarm_config.agent_number = agent_number
        
        self._config        = Configuration()
        
        for i in range(self._swarm_config.agent_number):
            None
            agent = Agent()
            agent.setSwarmConfig(self._swarm_config)
            self._agents.append(agent)
            
        for agent in self._agents:
            None
            agent.start()
        for agent in self._agents:
            None
            agent.join()
        
        print('Main Terminating...')
        
    def closeSwarm(self):
        self.agentStoryDB()
    
    def agentStoryDB(self):
        agents = self._mongo.getAgentQuery({'active': True})
        now = datetime.datetime.now()
        for agent in agents:
            print 'agent name',agent['name']
            self._mongo.endAgent(agent['name'], now.strftime("%Y-%m-%d %H:%M:%S"))
        
    def populationDB(self,db_reset=False):
        
        if db_reset == True:
            self._mongo.removeUsers({})
            self._mongo.removeWishList({})
        
        if len(self._mongo.getUsersQuery({})) == 0:
            
            # insert User
            user_id = self._mongo.insertUser('glaucomunsberg@gmail.com', 'Glauco Roberto', True, '100000197237018', None, self._helper.getTimeNow() )
            # insert examples into Wish List
            self._mongo.insertWishList(-31.777381, -52.340547, self._helper.getTimeNow(), user_id, False, False, 0.8, 'R. Uruguai', 'pelotas', 'brazil')
            self._mongo.insertWishList(-31.776393,-52.3424553, self._helper.getTimeNow(), user_id, False, False,0.2,'Gonçalves Chaves', 'pelotas', 'brazil')
            self._mongo.insertWishList(-31.744377,-52.3309687, self._helper.getTimeNow(), user_id, False, False, 0.2, 'Av. Jucelino K. de Oliveira', 'pelotas', 'brazil')
            self._mongo.insertWishList(-31.775344,-52.3445952, self._helper.getTimeNow(), user_id, False, False, 0.3, 'R. Gomes Carneiro', 'pelotas', 'brazil')
            self._mongo.insertWishList(-31.743544, -52.391601, self._helper.getTimeNow(), user_id, False, False, 0.5, 'R. Major Francisco N de Souza', 'pelotas', 'brazil')
            
#
# This class help the swarm to understand
#   the configuration of ambient and the
#   agent information
class SwarmConfig:
    
    host            = None
    identifier      = None
    agent_number    = 3
    
    def __init__(self):
        now = datetime.datetime.now()
        self.identifier = now.strftime("%Y%m%d%H%M%S")
        self.host       = socket.gethostbyname(socket.gethostname())
        
        print 'Swarm Configuration'
        print 'Identifier: ',self.identifier
        print 'Host      : ',self.host
        