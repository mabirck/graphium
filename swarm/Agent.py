#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, json, random, time, datetime

from threading import Thread
from geopy.distance import great_circle

from system.Configuration import *
from system.Mongo import Mongo
from Swarm import *
from API import *

class Agent(Thread):
    
    _config         = None
    _swarm_config   = None
    _mongo          = None
    _api            = None
    
    _work           = None
    _cicles         = None
    
    _agent_at_mongo = None
    _street         = None
    
    _node_osm           = None
    _node_osm_position  = None
    
    
    
    
    def __init__(self):
        Thread.__init__(self)
        self._config    = Configuration()  
        self._mongo     = Mongo()
        self._api       = API()
        self._work      = True
        self._cicles    = 0
        
    def run(self):
        
        self.startAgent()
        
        try:
            while self._work and self._cicles < 100:
                
                if 'last_street_id_osm' not in self._agent_at_mongo.keys():
                    self._agent_at_mongo['last_street_id_osm'] = None
                    
                if self._agent_at_mongo['last_street_id_osm'] == None:
                    
                    # search all possible streets
                    streets = self._mongo.getStreetQuery({'name_osm':{'$ne':""},'busy':{'$ne':True}})
                    
                    # rand a street between all
                    self._street = random.randint(0, len(streets)-1)
                    self._street = streets[self._street]
                    self._agent_at_mongo['last_street']         = self._street['name_osm']
                    self._agent_at_mongo['last_street_id_osm']  = self._street['id_osm']
                    self._street['busy'] = True
                    
                    # update list of streets visited
                    self.appendStreetVisited(self._street['name_osm'])
                    
                    # get the first node
                    self._node_osm_position = 0
                    self._node_osm = self._street['nodes'][self._node_osm_position]
                    
                    # update the last lat/lng of agent
                    self.appendLatLng(self._node_osm['lat'],self._node_osm['lng'],True)
                    
                    # update the street
                    self.updateCounter()
                    print('%s: find the street \'%s\' and id %s to start! :D' % (self.getName(),self._street['id_osm'],self._agent_at_mongo['last_street']))
                else:  
                    # if the node is the only on street
                    #   change the street or restart the node no aleatory position
                    #
                    # elif the street have only two dots or if the node is the last of the street
                    #   we need to change of street on the second node
                    #
                    # else
                    #   
                    if len(self._street['nodes']) == 1:
                        print('%s: we need change the street :]' % (self.getName()))
                        
                        streets_returneds = self._api.getWaysByNode(self._street['nodes'][0]['id'])
                        
                        # this dot has a second street
                        #   we choise with the street with less weight
                        if len(streets_returneds) != 1:
                            print('%s: choosing a new street... :)' % (self.getName()))
                            self.choosingNewStreetToNavegate(streets_returneds)
                        else:
                            #if number of nodes are diferent that 1 randint len
                            #   to find a new streets
                            if len(streets_returneds[0]['nodos']) != 1:
                                print('%s: I can\'t go to any way! A need restart at somewere :O' % (self.getName()))
                                streets_returneds = self._api.getWaysByNode(streets_returneds[0]['nodos'][randint(0,len(streets_returneds[0]['nodos'])-1)])
                                if len(streets_returneds) != 1:
                                    print('%s: choosing a new street... :)' % (self.getName()))
                                    self.choosingNewStreetToNavegate(streets_returneds)
                                else:
                                    print('%s: I can\'t go to any way! A need restart at somewere :O' % (self.getName()))
                                    self._agent_at_mongo['last_street_id_osm'] = None
                            else:
                                print('%s: II can\'t go to any way! A need restart at somewere :O' % (self.getName()))
                                self._agent_at_mongo['last_street_id_osm'] = None
                        
                    elif len(self._street['nodes']) == 2 or self._node_osm_position == len(self._street['nodes'])-2:
                        print('%s: process, but we need change the street =S' % (self.getName()))
                        # cal de distance between nodes
                        
                        self._node_osm = self._street['nodes'][self._node_osm_position]
                        self.appendLatLng(self._node_osm['lat'],self._node_osm['lng'],False)
                        
                        lat1 = float(self._node_osm['lat'])
                        lng1 = float(self._node_osm['lng'])
                        lat2 = float(self._street['nodes'][self._node_osm_position+1]['lat'])
                        lng2 = float(self._street['nodes'][self._node_osm_position+1]['lng'])
                        self.calculateDistanceMeters(lat1,lng1,lat2,lng2)
                        print('%s: Calculate the distance to %s and %s'%(self.getName(),self._street['nodes'][self._node_osm_position]['id'],self._street['nodes'][self._node_osm_position+1]['id']))
                        
                        
                        self._node_osm_position+=1
                        # update the value of this node
                        self.updateCounter()
                        
                        
                        # now we need change the street
                        streets_returneds = self._api.getWaysByNode(self._street['nodes'][self._node_osm_position]['id'])
                        the_last_weight = self._config.inf_positive
                        # this dot has a second street
                        #   we choise with the street with less weight
                        if len(streets_returneds) != 1:
                            print('%s: choosing a new street... :)' % (self.getName()))
                            self.choosingNewStreetToNavegate(streets_returneds)
                        else:
                            print('%s: I can\'t go to any way! A need restart at somewere :O' % (self.getName()))
                            self._agent_at_mongo['last_street_id_osm'] = None
                        
                    else:
                        
                        # cal de distance between nodes
                        print('%s: Calculate the distance to %s and %s'%(self.getName(),self._street['nodes'][self._node_osm_position]['id'],self._street['nodes'][self._node_osm_position+1]['id']))
                        
                        self._node_osm = self._street['nodes'][self._node_osm_position]
                        self.appendLatLng(self._node_osm['lat'],self._node_osm['lng'],False)
                        
                        distance = self.calculateDistanceMeters( float(self._node_osm['lat']), float(self._node_osm['lng']), float(self._street['nodes'][self._node_osm_position+1]['lat']), float(self._street['nodes'][self._node_osm_position+1]['lng']) )
                        
                        # update the set the next node of the street
                        self._node_osm_position+=1
                        self._node_osm = self._street['nodes'][self._node_osm_position]
                        
                        #update the visitation on this node
                        self.updateCounter()
                        
                        
                self._cicles +=1
                print('%s: cicle %s end' % (self.getName(),self._cicles))
                
                
            print('Agent %s' % (self.getName()))
            secondsToSleep = random.randint(1, 5)
            print('%s sleeping fo %d seconds...' % (self.getName(), secondsToSleep))
            time.sleep(secondsToSleep)
            
        #except Exception, e:
        #    print('Agent %s die! :/' % (self.getName())) 
        #    print e
        finally:
            self.endAgent()
            
            
    #
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
                print('%s: I NOT FIND THIS WAY %s :((' % (self.getName(),street_returned['id']))
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
        print('%s: the new street is \'%s\' and id %s ;)' % (self.getName(),self._street['name_osm'],self._street['id_osm']))
        
        # update the last lat/lng of agent
        self.appendLatLng(self._node_osm['lat'],self._node_osm['lng'],True)

        # update the street
        self.updateCounter()
        
        
    #
    # calculateDistanceMeters
    #   calcule the distance between two dots in meters
    #
    def calculateDistanceMeters(self,lat1,lng1,lat2,lng2):
        dot1 = (lat1,lng1)
        dot2 = (lat2,lng2)
        result = great_circle(dot1, dot2).meters
        print('%s the distance is %s =D' % (self.getName(),result))
        return result
    
    
    #
    # updateTheCounter
    #   update the counter on node atual
    #
    def updateCounter(self):
        
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
    # updateLatLng
    #   update the lat and lng of agent
    #   set at pathbread of agent
    #
    def appendLatLng(self,lat,lng,jump=False):
        self._agent_at_mongo['last_lat'] = lat
        self._agent_at_mongo['last_lng'] = lng
        self._agent_at_mongo['pathbread'].append({'lat':lat,'lng':lng,'jump':jump})
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
        
        identifier = self._mongo.insertAgent(self.getName(),self._swarm_config.host,self._swarm_config.identifier)
        self.setIdentifier(identifier)
        self._agent_at_mongo = self._mongo.getAgentByIdentifier(self.identifier)
        
        
    #
    # endAgent
    #   Set information about agent at db
    #   and close at db
    #
    def endAgent(self):
        now = datetime.datetime.now()
        self._agent_at_mongo['end_at'] = now.strftime("%Y-%m-%d %H:%M:%S")
        self._agent_at_mongo['active'] = False
        self._mongo.updateAgentByIdentifier(self.identifier,self._agent_at_mongo)
        
        
    #
    # setSwarmConfig
    #   set swarmconfig to get a lot
    #   of information about the swarm
    #   and the configuration
    #
    def setSwarmConfig(self,swarm_config):
        self._swarm_config = swarm_config
    
    
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
    

        