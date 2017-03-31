#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo, datetime,bson,time

from random import randint
from unidecode import unidecode
from pymongo import MongoClient
from bson.objectid import ObjectId

from Configuration import Configuration
class Mongo:

    config		= None

    __client	= None
    __db 		= None
    __collection= None

    def __init__(self,db='graphium',address='localhost',port=27017):

        self.config 		= Configuration()
        self.__client		= MongoClient(self.config.mongo_host, self.config.mongo_port)
        self.__db			= self.__client[self.config.mongo_db]
        self.__collection   = self.__db.agent_story

        
    ############ Agent ############
    
    # getAgentByIdentifier
    #   permit to update informatations at mongodb
    #
    def getAgentByIdentifier(self,identifier):
        self.__collection   = self.__db.agent_story
        return self.__collection.find_one({'identifier':identifier})
    
    # getAgent
    #   set the end information about the agent
    #   
    def getAgentByName(self,agent_name):
        self.__collection   = sef.__db.agent_story
        return self.__collection.find_one({'agent_name':agent_name})
    
    
    # updateAgentByName
    #   permit to update informatations at mongodb
    #
    def updateAgentByName(self,agent_name,data):
        self.__collection = self.__db.agent_story
        self.__collection.update({'name':agent_name},{"$set":data},upsert=False)
        
    # updatePathAgentById
    #   permit to update informatations at mongodb
    #
    def updateAgentByIdentifier(self,identifier,data):
        self.__collection = self.__db.agent_story
        self.__collection.update({'identifier':identifier},{"$set":data},upsert=False)
    
    # insertAgent
    #   insert the agent atMongoDB
    #
    def insertAgent(self,name,host,swarm_identifier,color=None):
        now = datetime.datetime.now()
    
        identifier = now.strftime("%Y%m%d%H%M%S%f")[:-3]
        if color == None:
            colors = self.config.colors
            active_agents = len(self.getAgentQuery({'active': True}))
            if len(colors) <= active_agents :
                color = colors[active_agents-1]
            else:
                color = colors[randint(0,len(colors)-1)]
        
        dataToSend = { 'identifier':identifier, 'name':name, 'host':host, 'swarm_identifier':swarm_identifier,'color':color, 'active':True, 'end_at':None, 'last_lat':0.0, 'last_lng':0.0, 'last_street':None,'pathbread':[],'visited_streets':[],'busy':False}
        self.__collection = self.__db.agent_story
        the_id = self.__collection.insert(dataToSend)
        return identifier
    
    # endAgent
    #   set the end information about the agent
    # 
    def endAgent(self,identifier,end_at):
        self.__collection = self.__db.agent_story
        self.__collection.update({'identifier':identifier},{"$set":{'end_at':end_at,'active':False}},upsert=False)
    
    # getAgentsBySwarmIndentifier
    #   return all agente by swarm identifier
    #
    def getAgentsBySwarmIdentifier(self,swarm_identifier):
        returned = []
        self.__collection   = self.__db.agent_story
        return list(self.__collection.find({'swarm_identifier':swarm_identifier}).short("_id"))
        
    # getAgentQuery
    #   return the users basead on query passed
    #
    def getAgentQuery(self,query={}):
        self.__collection = self.__db.agent_story
        return list(self.__collection.find(query))
    
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
        self.__collection   = sef.__db.agent_story
        return self.__collection.find({'name_osm':street_name})
    
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