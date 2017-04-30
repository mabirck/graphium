#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pymongo, datetime, bson, time
from pymongo import MongoClient
from bson.objectid import ObjectId

class Mongo:

    __client	= None
    __db 		= None
    __collection= None

    
    def __init__(self,db='graphium',address='localhost',port=27017):

        self.__client		= MongoClient(address, port)
        self.__db			= self.__client[db]
        self.__collection   = self.__db.agent
    
    ############ Crawler Session ############
    
    # insertCrawlerSession
    #   create a session of swarm and send the basic information
    #   return session ID
    #
    def insertCrawlerSession(self, identifier, tags, start_at, end_at="", end_well=False, total_images=0, total_processed=0, total_pages=1,current_page=1):
        self.__collection = self.__db.crawler_session
        dataToSend = {'identifier':identifier, 'tags':tags, 'start_at':start_at, 'end_at':end_at, 'end_well':end_well, 'total_images':total_images, 'total_processed':total_processed, 'total_pages':total_pages, 'current_page':current_page, 'active':True}
        return self.__collection.insert_one(dataToSend).inserted_id
    
    # getCrawlerSessions
    #   return the sessions basead on query passed
    #
    def getCrawlerSessions(self,query={}):
        self.__collection = self.__db.crawler_session
        return list(self.__collection.find(query))
    
    # updateCrawlerByIdentifier
    #   permit to update informatations at mongodb
    #
    def updateCrawlerByIdentifier(self,identifier,data):
        self.__collection = self.__db.crawler_session
        self.__collection.update({'identifier':identifier},{"$set":data},upsert=False)
    
    # getCrawlerById
    #   return session based on identifier
    #
    def getCrawlerById(self,identifier):
        self.__collection = self.__db.crawler_session
        return self.__collection.find_one({'identifier':identifier})
    
    
    ############ Image ############
    
    # getImages
    #   return all imagens that match with query
    #
    def getImages(self,query={}):
        self.__collection = self.__db.crawler_image
        return list(self.__collection.find(query))
    
    # updateCrawlerByIdentifier
    #   permit to update informatations at mongodb
    #
    def updateImageByIdentifier(self,identifier,data):
        self.__collection = self.__db.crawler_image
        self.__collection.update({'identifier':identifier},{"$set":data},upsert=False)
    
    # getFlickrImageById
    #   return a image or null basead on image_id passed
    #
    def getFlickrImageById(self,image_id):
        self.__collection = self.__db.crawler_image
        return self.__collection.find_one({'image_ficker_id':image_id})
     
    # insertFlickrImage
    #   create a session of swarm and send the basic information
    #   return session ID
    #
    def insertFlickrImage(self, identifier, flickr_image_id, sessions=[], created_at="", width="", height="", data_url="", photopage="", repository_url="",visibility_public=True):
        dataToSend = {'identifier':identifier, 'flickr_image_id':flickr_image_id, 'sessions':sessions, 'created_at':created_at, 'width':width, 'height':height, 'repository_url':repository_url, 'data_url':data_url, 'visibility_public':visibility_public}
        self.__collection = self.__db.crawler_image
        return self.__collection.insert_one(dataToSend).inserted_id
    
    def disconnect(self):
        self.__client.close()