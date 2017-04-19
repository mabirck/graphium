#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, json, random, time, traceback
from threading import Thread
from geopy.distance import great_circle

from system.Configuration import *
from system.Mongo import *
from system.Logger import *
from system.Helper import *
from Swarm import *
from API import *

class Agent(Thread):
    
    _config         = None
    
    _mongo          = None
    _api            = None
    _logger         = None
    _helper         = None
    
    _work           = None
    _cicles         = None
    
    _agent_at_mongo = None
    _swarm_at_mongo = None
    _street         = None
    
    _swarm_identifier   = None
    _node_osm           = None
    _node_osm_position  = None
      
    
    def __init__(self,swarm_identifier):
        Thread.__init__(self)
        
        self._config    = Configuration()  
        self._mongo     = Mongo()
        self._api       = API()
        self._logger    = Logger(swarm_identifier)
        self._helper    = Helper()
        
        self._swarm_identifier  = swarm_identifier
        self._swarm_at_mongo    = self._mongo.getSwarmByIdentifier(swarm_identifier)
        self._continue_the_job  = True
        self._end_well          = True
        self._cicles            = 0
        
        self.startAgent()
        
        self._logger.info('%s: Hello! I\'m ready! ;)' % (self.getName()))
        
        
    def run(self):
        
        try:
            self._logger.info('%s: Let start the job! =D' % (self.getName()))
            while self._continue_the_job:
                        
                # if not set the last street
                #   this agent need choose one street to start
                #   else need to get from chooseTheNextStreet
                if self._agent_at_mongo['last_street_id_osm'] == None:
                    self._street = self.chooseTheFirstStret()
                else:  
                    self._street = self.chooseTheNextStreet()
                
                self._agent_at_mongo['last_street']         = self._street['name_osm']
                self._agent_at_mongo['last_street_id_osm']  = self._street['id_osm']
                self._street['busy'] = True

                self.appendStreetVisited(self._street['name_osm'])

                self._logger.info('%s: find the street \'%s\' and id %s to start! :D' % (self.getName(),self._street['id_osm'],self._agent_at_mongo['last_street']))
                

                # if this street never was visited need to
                #   to calculate the cross street by him
                if len(self._street['cross_streets_osm_id']) == 0:
                    cross_streets_osm_id = []

                    # from any node of this street we get all street crossed by him
                    for node in self._street['nodes']:
                        streets_returneds = self._api.getWaysByNode(node['id'])
                        for street_returned in streets_returneds:
                            cross_streets_osm_id.append(street_returned['id'])

                    # remove all duplicate ids
                    cross_streets_osm_id = list(set(cross_streets_osm_id))

                    #remove this stret id because the street can't cross youself
                    #   but the nodes will cross this street id (all of them)
                    cross_streets_osm_id.remove(self._street['id_osm'])
                    self._street['cross_streets_osm_id'] = cross_streets_osm_id
                    self._mongo.updateStreetById(self._street.get('_id'),self._street)
                    
                    # update the last lat/lng of agent
                    
                
                # if that street thas only one node
                #   it is a problem! Cannot run inside him
                if len(self._street['nodes']) == 1:
                    
                    self._node_osm = self._street['nodes'][self._node_osm_position]
                    
                    self.oneNode(self._node_osm)
                    # update the street counter
                    # read more at updateRule
                    self.updateRule()
                else:
                    self._node_osm_position=-1 # on start of array of nodes
                    for node in self._street['nodes']:
                        self._node_osm_position+=1
                        self._node_osm = self._street['nodes'][self._node_osm_position]
                        
                        # update the street counter
                        # read more at updateRule
                        self.updateRule()
                        
                        if self._node_osm_position != 0 and self._node_osm_position <= len(self._street['nodes'])-2:

                            # call the method that execute something node by node
                            self.nodeByNode(self._node_osm,self._street['nodes'][self._node_osm_position+1])

                        else:
                            if self._node_osm_position == 0:
                                # set the visit of this node
                                self.firstNode(self._node_osm)
                            else:
                                self.lastNode(self._node_osm)
                        
                
                # check if number of threads is upper than necessary
                num_active_agent = len(self._mongo.getAgentsActiveBySwarm(self._swarm_identifier))
                self._swarm_at_mongo = self._mongo.getSwarmByIdentifier(self._swarm_identifier)
                
                num_agent_by_swarm = self._swarm_at_mongo['num_agent']
                swarm_active = self._swarm_at_mongo['active']
                swarm_cicles = self._swarm_at_mongo['cycles_number']
                if num_active_agent > num_agent_by_swarm:
                    self._logger.info('%s: I need stop my job!' % (self.getName()))
                    self._continue_the_job = False
                    
                if swarm_cicles > 0 and swarm_cicles <= self.cicles:
                    self._logger.info('%s: I need stop my job! Cicles end' % (self.getName()))
                    self._continue_the_job = False
                    
                if swarm_active == False:
                    self._logger.info('%s: I need stop my job! The swarm end' % (self.getName()))
                    self._continue_the_job = False
                        
                self._cicles +=1
                self._logger.info('%s: the cicle %s end' % (self.getName(),self._cicles))
                
                
            print('Agent %s ending' % (self.getName()))
            #secondsToSleep = random.randint(1, 5)
            #print('%s sleeping fo %d seconds...' % (self.getName(), secondsToSleep))
            #time.sleep(secondsToSleep)
            
        except Exception as error:
            self._logger.error('%s: Agent die! x(' % (self.getName()))
            print 'Error:'
            print traceback.format_exc()
            self._logger.critical(str(error))
            self._end_well = False
        finally:
            self.finish()
            
    #
    # updateRule
    #   the update rule is the way that way
    #   set the value. This code use "Node Counting"
    #   read more about other methods to update at "Terrain Coverage with UAVs: Real-time Search and Geometric Approaches Applied to an Abstract Model of Random Events"
    #
    def updateRule(self):
        
        # update the node count
        if 'node_count' in self._node_osm.keys():
            self._node_osm['node_count'] += 1
        else:
            self._node_osm['node_count'] = 1

        # update the street count
        if 'street_count' in self._street.keys():
            self._street['street_count'] += 1
        else:
            self._street['street_count'] = 1
        self._mongo.updateStreetById(self._street.get('_id'),self._street)
        
    #
    # nodeByNode
    #   calcule the distance between two dots in meters
    #
    def nodeByNode(self,this_node,next_node):
        
        self.appendPathBread(this_node['id'],this_node['lat'],this_node['lng'],False)
    
        lat1 = float(this_node['lat'])
        lng1 = float(this_node['lng'])
        lat2 = float(next_node['lat'])
        lng2 = float(next_node['lng'])
        
        dot1 = (lat1,lng1)
        dot2 = (lat2,lng2)
        
        result = great_circle(dot1, dot2).meters
        
        self._logger.info('%s: The distance from %s to %s is %s! :P'%(self.getName(),this_node['id'],next_node['id'],result))
        
        return result
    
    #
    # firstNode
    #   execute only on first node
    #
    def firstNode(self,first_node):
        self.appendPathBread(first_node['id'],first_node['lat'],first_node['lng'],False)            
        self._logger.info('%s: It is the first node with id %s :T' % (self.getName(),first_node['id']))
    
    #
    # lastNode
    #   execute only on last node
    #
    def lastNode(self,last_node):
        self.appendPathBread(last_node['id'],last_node['lat'],last_node['lng'],True)
        self._logger.info('%s: It is the last node of this street with id %s :)' % (self.getName(),last_node['id']))
        self._street['busy'] = False
     
    #
    # oneNode
    #   call when we have only one node at street
    #
    def oneNode(self,the_node):
        self.appendPathBread(the_node['id'],the_node['lat'],the_node['lng'],False)
        self.appendPathBread(the_node['id'],the_node['lat'],the_node['lng'],True)
        self._street['busy'] = False

        self._logger.info('%s: I can\'t run on this street! Only one node :S' % (self.getName()))
    #
    # chooseTheFirstStret
    #   Method to choose the first street
    #   to try walk. First choose a way from 
    #   wishlist else a aleatory way
    #
    def chooseTheFirstStret(self):
        
        # search all possible streets that are not busy
        wishlist = self._mongo.getWishListNoProccessedByIdentifier(self._swarm_identifier)
        if len(wishlist) == 0:
            self._logger.info('%s: Wishlist is processed I will get a random street :]' % (self.getName()))
            streets = self._mongo.getStreetQuery({'name_osm': {'$ne':""}, 'busy':{'$ne':True}, 'city_id': self._swarm_at_mongo['city_id']})

            # rand a street between all
            return streets[random.randint(0, len(streets)-1)] 
        else:
            self._logger.info('%s: Wishlist has a street OSM ID %s to by processed ;)' % (self.getName(),wishlist[0]['osm_way_id']))
            street = self._mongo.getStreetByIdOSM(int(wishlist[0]['osm_way_id']))
            print 'street returned'
            print street
            return street
    #
    # after walk one street new need choose de next
    #   this method choose the way with less count
    #   and return. If any way cross he then we need
    #   get other way how? Go to other agent =]
    #   algorithm
    #       close the corrent street
    #       find the street with less count
    #       if not find any street
    #       
    def chooseTheNextStreet(self):
        
        the_street_chosen = None
        the_last_weight = self._config.inf_positive
        self._mongo.updateStreetById(self._street.get('_id'),self._street)
        
        for street_id in self._street['cross_streets_osm_id']:
            street = self._mongo.getStreetByIdOSM(int(street_id))
            street_count = 0
            if street == None:
                self._logger.info('%s: I cannot find this way %s :((' % (self.getName(),street_id))
            else:
                if not street['busy']:
                    street_count = street['street_count']
                    if the_last_weight > street_count:
                        the_last_weight = street_count
                        the_street_chosen = street
        if the_street_chosen != None:
            return the_street_chosen
        else:
            # if any street was selected from current street 
            #   we try to get the first street with the less value
            #   at one of all agents of swarm.
            #   then choose a random street
            self._logger.info('%s: I cannot find any way. Let me help other agent :/' % (self.getName()))
            agents = self._mongo.getAgentsBySwarmIdentifier(self._swarm_identifier)
            agents = random.shuffle(agents)
            agent_visited=0
            the_agent_chosen = None
            while the_street_chosen == None or agents_visited != len(agents):
                agent = agents.get(agent_visited)
                if agent['last_street_id_osm'] != None and agent['active']:
                    the_last_weight = self._config.inf_positive
                    street_id = agent['last_street_id_osm']
                    street = self._mongo.getStreetByIdOSM(int(street_id))
                    street_count = 0
                    if street == None:
                        self._logger.info('%s: I cannot find this way %s :((' % (self.getName(),street_id))
                    else:
                        if not street['busy']:
                            street_count = street['street_count']
                            if the_last_weight > street_count:
                                the_last_weight = street_count
                                the_street_chosen = street
                                the_agent_chosen = agent['name']
                                
                agents_visited+=1
                
            if the_street_chosen != None:
                self._logger.info('%s: I will help the %s agent *_*' % (self.getName(),the_agent_chosen))
                return the_street_chosen
            else:
                self._logger.info('%s: Oh really? I will check wishlist or get a random way -.-' % (self.getName()))
                return self.chooseTheFirstStret()
                
                
    # choosingNewStreetToNavegate
    #   choose the street with the less weight
    #   to navegate
    #
    def choosingNewStreetToNavegate(self,streets_returneds):
        the_street_chosen = None
        the_last_weight = self._config.inf_positive
        
        for street_returned in streets_returneds:
            street = self._mongo.getStreetByIdOSM(int(street_returned['id']))
            street_count = 0
            if street == None:
                self._logger.info('%s: I NOT FIND THIS WAY %s :((' % (self.getName(),street_returned['id']))
            else:
                if 'street_count' in street.keys():
                    street_count = street['street_count']
                if the_last_weight > street_count:
                    the_last_weight = street_count
                    the_street_chosen = street
        # the 'the_street_chosen' is the new street to see
        # we need close current street
        self._street['busy'] = False
        self._mongo.updateStreetById(self._street.get('_id'),self._street)
        
        # we need set the current street with 'the_street_chose'
        #   update the agent the agent information
        self._street = the_street_chosen
        self._street['busy'] = True

        self._agent_at_mongo['last_street_id_osm'] = self._street['id_osm']
        self._agent_at_mongo['last_street'] = self._street['name_osm']
        
        # update list of streets visited
        self.appendStreetVisited(self._street['name_osm'])
        
        # get the first node
        self._node_osm_position = 0
        self._node_osm = self._street['nodes'][self._node_osm_position]
        self._logger.info('%s: the new street is \'%s\' and id %s ;)' % (self.getName(),self._street['name_osm'],self._street['id_osm']))
        
        # update the last lat/lng of agent
        self.appendPathBread(self._node_osm['id'],self._node_osm['lat'],self._node_osm['lng'],True)

        # update the street
        self.updateRule()
    

    #
    # updateLatLng
    #   update the lat and lng of agent
    #   set at pathbread of agent
    #
    def appendPathBread(self,node_id,lat,lng,jump=False):
        self._agent_at_mongo['last_lat'] = lat
        self._agent_at_mongo['last_lng'] = lng
        self._agent_at_mongo['pathbread'].append({'node_id':node_id,'lat':lat,'lng':lng,'jump':jump})
        self._mongo.updateAgentByIdentifier(self.identifier,self._agent_at_mongo)
    
    #
    # appendStreetVisited
    #   insert the name of the street if agent
    #   are not visited yet
    #
    def appendStreetVisited(self,street_name):
        
        if street_name not in self._agent_at_mongo['visited_streets']:
            self._agent_at_mongo['visited_streets'].append(street_name)
            self._mongo.updateAgentByIdentifier(self.identifier,self._agent_at_mongo)
    
    #
    # startAgent
    #   Set the name, start the mongo
    #   information and others actions
    #
    def startAgent(self):
        
        self.setAgentName()
        
        identifier = self._mongo.insertAgent(self.getName(),self._swarm_identifier)
        self.setIdentifier(identifier)
        self._agent_at_mongo = self._mongo.getAgentByIdentifier(self.identifier)
        
        
    #
    # finish
    #   Set information about agent at db
    #   and close at db
    #
    def finish(self):
        self._agent_at_mongo['end_at']      = self._helper.getTimeNow()
        self._agent_at_mongo['active']      = False
        self._agent_at_mongo['end_well']    = self._end_well
        self._agent_at_mongo['cicles']      = self._cicles
        self._mongo.updateAgentByIdentifier(self.identifier,self._agent_at_mongo)
        
        if self._street != None:
            self._street['busy'] = False
            self._mongo.updateStreetById(self._street.get('_id'),self._street)
        else:
            self._logger.info('%s: I finish without update the street value :)' % (self.getName()))
        
    #
    # getIdentifier
    #
    def getIdentifier(self):
        return self.identifier
    
    
    #
    # setIndetifier
    #
    def setIdentifier(self,identifier):
        self.identifier = identifier 
        
        
    #
    # setAgentName
    #   def a cut name to agent <3
    #
    def setAgentName(self):
        
        url = self._config.swarm_agent_names_API
        response = urllib.urlopen(url)
        try:
            data = json.loads(response.read())
            self.setName(data[0])
        except URLError as e:
            self.setName(self._config.swarm_agent_names[random.randint(0, len(self._config.swarm_agent_names)-1)])
    

        