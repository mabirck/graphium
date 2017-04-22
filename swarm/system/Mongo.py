#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo, datetime,bson,time
import system
from random import randint
from unidecode import unidecode
from pymongo import MongoClient
from bson.objectid import ObjectId
from system.Configuration import *

class Mongo:

    __client	= None
    __db 		= None
    __collection= None

    
    def __init__(self,db='graphium',address='localhost',port=27017):

        self.__client		= MongoClient(address, port)
        self.__db			= self.__client[db]
        self.__collection   = self.__db.agent
        
        
    def disconnect(self):
        self.__client.close()

        
    ############ Agent ############
    
    # getAgentByIdentifier
    #   permit to update informatations at mongodb
    #
    def getAgentByIdentifier(self,identifier):
        self.__collection   = self.__db.agent
        return self.__collection.find_one({'identifier':identifier})
    
    # getAgent
    #   set the end information about the agent
    #   
    def getAgentByName(self,agent_name):
        self.__collection   = sef.__db.agent
        return self.__collection.find_one({'agent_name':agent_name})
    
    
    # updateAgentByName
    #   permit to update informatations at mongodb
    #
    def updateAgentByName(self,agent_name,data):
        self.__collection = self.__db.agent
        self.__collection.update({'name':agent_name},{"$set":data},upsert=False)
        
    # updatePathAgentById
    #   permit to update informatations at mongodb
    #
    def updateAgentByIdentifier(self,identifier,data):
        self.__collection = self.__db.agent
        self.__collection.update({'identifier':identifier},{"$set":data},upsert=False)
    
    # insertAgent
    #   insert the agent atMongoDB
    #
    def insertAgent(self,name,swarm_identifier,color=None):
        now = datetime.datetime.now()
        
        self.config = system.Configuration.Configuration()
        identifier = now.strftime("%Y%m%d%H%M%S%f")[:-3]
        if color == None:
            colors = self.config.swarm_agent_colors
            active_agents = len(self.getAgentQuery({'active': True}))
            if len(colors) <= active_agents :
                color = colors[active_agents-1]
            else:
                color = colors[randint(0,len(colors)-1)]
        
        dataToSend = { 'identifier':identifier, 'name':name, 'swarm_identifier':swarm_identifier,'color':color, 'active':True, 'end_at':None, 'last_lat':0.0, 'last_lng':0.0, 'last_street':None,'pathbread':[],'visited_streets':[],'last_street_id_osm':None,'cycles':0}
        self.__collection = self.__db.agent
        the_id = self.__collection.insert(dataToSend)
        return identifier
    
    # endAgent
    #   set the end information about the agent
    # 
    def endAgent(self,identifier,end_at):
        self.__collection = self.__db.agent
        self.__collection.update({'identifier':identifier},{"$set":{'end_at':end_at,'active':False}},upsert=False)
    
    # getAgentsBySwarmIndentifier
    #   return all agente by swarm identifier
    #
    def getAgentsBySwarmIdentifier(self,swarm_identifier):
        returned = []
        self.__collection   = self.__db.agent
        return list(self.__collection.find({'swarm_identifier':swarm_identifier}).short("_id"))
        
    # getAgentQuery
    #   return the users basead on query passed
    #
    def getAgentQuery(self,query={}):
        self.__collection = self.__db.agent
        return list(self.__collection.find(query))
    
    
    def getAgentsActiveBySwarm(self,swarm_identifier):
        returned = []
        self.__collection   = self.__db.agent
        return list(self.__collection.find({'swarm_identifier':swarm_identifier,'active':True}))
    
    def getAgentsEndWellBySwarm(self,swarm_identifier):
        returned = []
        self.__collection   = self.__db.agent
        return list(self.__collection.find({'swarm_identifier':swarm_identifier,'end_well':True}))
    
	############ User ############

    # insertUser
    #   insert the user at MongoDB
    #   return the id
    #
    def insertUser(self,email,name,male,facebook_id,google_id,created_at):
        dataToSend = {'email':email, 'name':name, 'male':male, 'facebook_id':facebook_id, 'google_id':google_id, 'created_at': created_at}
        self.__collection = self.__db.user
        return self.__collection.insert_one(dataToSend).inserted_id
        
    # updateUserInformation
    #
    def updateUserInformation(self,email,data):
        self.__collection = self.__db.user
        self.__collection.update({'email':email},{"$set":data},upsert=False)
        
    # getUsersQuery
    #   return the users basead on query passed
    #
    def getUsersQuery(self,query={}):
        self.__collection = self.__db.user
        return list(self.__collection.find(query))
    
    # removeUsers
    #
    def removeUsers(self,query={}):
        self.__collection = self.__db.user
        self.__collection.remove(query)
    
    
    ############ Street ############
    
    # getStreetByIdOSM
    #   get street by id OSM of street
    #
    def getStreetByIdOSM(self,identifier):
        self.__collection   = self.__db.street
        return self.__collection.find_one({'id_osm':identifier})
    
    # getStreet
    #   set the end information about the street
    #   
    def getStreetByName(self,street_name):
        self.__collection   = self.__db.street
        return self.__collection.find_one({'name_osm':street_name})
    
    # updateStreetById
    #   permit to update informatations at mongodb
    #
    def updateStreetById(self,identifier,data):
        self.__collection = self.__db.street
        self.__collection.update({'_id':identifier},{"$set":data},upsert=False)
    
    # getStreetsQuery
    #   return the users basead on query passed
    #
    def getStreetQuery(self,query={}):
        self.__collection = self.__db.street
        return list(self.__collection.find(query))
    
    
    
    ############ WishList ############
    
    # insertWishList
    #   return ID
    #
    def insertWishList(self,lat,lng,dt_required,user_id,busy,processed,priority,street_name,city,country):
        dataToSend = {'lat':lat, 'lng':lng, 'dt_required':dt_required, 'user_id':user_id, 'busy':busy, 'processed': processed, 'priority':priority, 'street_name':street_name, 'city':city, 'country':country}
        self.__collection = self.__db.wish_list
        return self.__collection.insert_one(dataToSend).inserted_id
    
    # remove WishList
    #
    def removeWishList(self,query={}):
        self.__collection = self.__db.wish_list
        self.__collection.remove(query)
    
    # getWishListById
    #
    def getWishListById(self,wishListId):
        self.__collection = self.__db.wish_list
        return self.__collection.find_one({'_id':wishListId})
    
    
    ############ Configuration ############
    
    # insertConfiguration
    #   return ID
    #
    def insertConfiguration(self, swarm_agent_number=3, swarm_agent_names_API="http://namey.muffinlabs.com/name.json?with_surname=true&frequency=all", swarm_agent_names = ['Coralina Malaya','Abigail Johnson','Antonietta Marinese','Elisa Rogoff','Serafim Folkerts','Dulce Barrell'], mongo_db = "graphium", mongo_host = "localhost", mongo_port = 27017, swarm_agent_colors = ["#E91E63", "#9C27B0", "#F44336", "#673AB7", "#3F51B5", "#2196F3", "#00BCD4", "#009688", "#4CAF50", "#CDDC39", "#FF9800","#795548","#FF5722","#607D8B","#9E9E9E","#827717"], inf_positive = 99999, inf_negative = -99999, osmapi_user = "glaucomunsberg", osmapi_password = "30271255",swarm_seconds_to_check_agents  = 3):
        dataToSend = {'swarm_agent_number':swarm_agent_number, 'swarm_agent_names_API':swarm_agent_names_API, 'swarm_agent_names':swarm_agent_names, 'mongo_db':mongo_db, 'mongo_host':mongo_host, 'mongo_port': mongo_port, 'swarm_agent_colors':swarm_agent_colors, 'inf_positive':inf_positive, 'inf_negative':inf_negative, 'osmapi_user':osmapi_user, 'osmapi_password': osmapi_password, 'swarm_seconds_to_check_agents': swarm_seconds_to_check_agents}
        self.__collection = self.__db.configuration
        return self.__collection.insert_one(dataToSend).inserted_id
    
    # insertConfiguration
    #   return configuration | None
    #
    def getConfiguration(self):
        self.__collection = self.__db.configuration
        configuration = list(self.__collection)
        if len(configuration) != 0:
            return configuration[0]
        else:
            return None
    
    

    ############ Session and Logger ############
    
    # insertSwarm
    #   create a session of swarm and send the basic information
    #   return session ID
    #
    def insertSwarm(self, identifier, num_agent,user_email="admin@graphium", name='default', host='0.0.0.0',  seconds_to_check_agents=3, cycles_number=-1, city_id=None, active=True, logs=[]):
        self.__collection = self.__db.swarm
        dataToSend = {'identifier':identifier, 'name':name, 'num_agent':num_agent, 'user_email':user_email, 'host':host, 'active':active, 'logs':[], 'end_at':None, 'end_well':True, 'qmi':0.0, 'seconds_to_check_agents': seconds_to_check_agents,'city_id':city_id,'cycles_number':cycles_number}
        return self.__collection.insert_one(dataToSend).inserted_id
    
    # getSwarmByIdentifier
    #   get the swarm session by identifier
    #
    def getSwarmByIdentifier(self,identifier):
        self.__collection   = self.__db.swarm
        return self.__collection.find_one({'identifier':identifier})
    
    # updateSwarmByIdentifier
    #   permit to update informatations at mongodb
    #
    def updateSwarmByIdentifier(self,identifier,data):
        self.__collection = self.__db.swarm
        self.__collection.update({'identifier':identifier},{"$set":data},upsert=False)
    
    # addLog
    #   adding on more log at one session
    #
    def addLog(self,message,level,swarm_session):
        self.__collection = self.__db.swarm
        swarm = self.__collection.find_one({'identifier':swarm_session})
        if swarm != None:
            swarm['logs'].append({'level':level,'message':message})
            self.__collection.update({'swarm_identifier':swarm_session},{"$set":swarm},upsert=False)
            
    
    
    ############ Wish List ############
    
    # updateWishById
    #   update a document from wish list by id
    #
    def updateWishById(self,mongo_id,data):
        self.__collection = self.__db.wish_list
        self.__collection.update({'_id':mongo_id},{"$set":data},upsert=False)
    
    # getWishListByIdentifier
    #   return the list of wishs by swarm
    #   short from priority
    #
    def getWishListByIdentifier(self,swarm_session):
        self.__collection = self.__db.wish_list
        return list(self.__collection.find({'swarm_identifier':swarm_session}).short("priority"))
    
    # getWishListByIdentifier
    #   return the list of wishs by swarm
    #
    def getWishListNoProccessedByIdentifier(self,swarm_session):
        self.__collection = self.__db.wish_list
        return list(self.__collection.find({'swarm_identifier':swarm_session,'processed':False}))
    
    # updateStreetById
    #   permit to update informatations at mongodb
    #
    def updateWishListById(self,identifier,data):
        self.__collection = self.__db.wish_list
        self.__collection.update({'_id':identifier},{"$set":data},upsert=False)