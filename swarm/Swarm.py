#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, datetime, traceback

from system.Configuration import *
from system.Mongo import *
from system.Helper import *
from system.Logger import *
from Agent import *

class Swarm:
    
    _agents         = []
    _config         = None
    _swarm_config   = None
    _mongo          = None
    _helper         = None
    _logger         = None
    _name           = None
    _end_well       = None
    _swarm_at_mongo = None

    def __init__(self, swarm_identifier=None, swarm_name=None, user_email=None):
        
        self._config        = Configuration()
        self._mongo         = Mongo()
        self._helper        = Helper()
        self._logger        = Logger(swarm_identifier)
        
        # start basic information about swarm session
        self._logger.debug('Swarm: We are configure my settings...')
        self.swarm_name         = swarm_name
        self._swarm_config      = SwarmConfig(swarm_identifier,swarm_name)
        self._swarm_config.agent_number = self._config.swarm_agent_number
        
        self._mongo.insertSession(self._swarm_config.identifier, self._config.swarm_agent_number, user_email, swarm_name, self._swarm_config.host)
        self._swarm_at_mongo    = self._mongo.getSwarmByIdentifier(self._swarm_config.identifier)
        
        
    # Start the agents 
    def start(self):
        
        self._logger.debug('Swarm: Let starting agents...')
        try:
            for i in range(self._swarm_config.agent_number):
                agent = Agent(self._swarm_config)
                self._agents.append(agent)

            for agent in self._agents:
                agent.start()

            for agent in self._agents:
                agent.join()
        except Exception as error:
            self._logger.error('Swarm: Swarm die! x(')
            print 'Error:'
            print traceback.format_exc()
            self._logger.critical(str(error))
            self._end_well = False
        finally:
            self.finish()
        
    def finish(self):
        self._swarm_at_mongo['end_at']      = self._helper.getTimeNow()
        self._swarm_at_mongo['active']      = False
        self._swarm_at_mongo['end_well']    = self._end_well
        
        self._mongo.updateSwarmByIdentifier(self._swarm_config.identifier,self._swarm_at_mongo)
        
        self._logger.info('Swarm: Hard work! I finish dude ;)')

#
# This class help agents to understand
#   the configuration of Swarm
#
class SwarmConfig:
    
    host            = None
    identifier      = None
    name            = None
    _helper         = None
    
    def __init__(self,identifier=None,name=None):
        
        self.name       = name
        if identifier == None:
            self._helper = Helper()
            self.identifier = self._helper.getSerialSwarmNow()
        else:
            self.identifier = identifier
        self.host       = socket.gethostbyname(socket.gethostname())
        print 'Swarm Configuration'
        print 'Identifier: ',self.identifier
        print 'Host      : ',self.host
        