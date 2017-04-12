#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import pymongo
from pymongo import MongoClient
from osgeo import ogr, osr
from osmread import parse_file, Way, Node,Relation

from Configuration import Configuration
class Reader:
    
    
    _config     = None
    file_name   = None
    nodes       = None
    city        = None
    
    def __init__(self):
        
        self._config    = Configuration()
        
        self.__client		= MongoClient(self._config.mongo_host, self._config.mongo_port)
        self.__db			= self.__client[self._config.mongo_db]
        self.__collection   = self.__db.street
        
        self.file_name  = None
        self.nodes      = {}
        self.ways_types = []
        self.num_total_ways = 0
        
        
    def osmToMongoDB(self,osm_file=None):
        
        if osm_file != None:
            self.file_name = osm_file
        else:
            self.file_name = self._config.osm_city_url
            
        city_exits = False
        # select the subtypes of streets to filter on osm file
        if self._config.use_urban_ways == True:
            self.ways_types += self._config.urban_highway_tipes
        if self._config.use_motorways  == True:
            self.ways_types += self._config.motorways_highway_tipes
        if self._config.use_othersways == True:
            self.ways_types += self._config.others_highway_tipes
           
        print 'types',self.ways_types
        # first is necessary map all nodes to fast acess on dict
                
        for entity in parse_file('data/ex_B5u65rYvSdtoSZj5oZqdqReaVrdsc.osm'):
            if isinstance(entity,Node):
                self.nodes[str(entity.id)] = entity
                
            if isinstance(entity,Node) and 'place' in entity.tags and entity.tags['place'] == "city":
                city = {}
                
                try:
                    city['name'] = entity.tags['name']
                except:
                    city['name'] = ""
                
                try:
                    city['state'] = entity.tags['is_in:state']
                except:
                    city['state'] = entity.tags['is_in']
                    
                try:
                    city['country'] = entity.tags['is_in:country']
                except:
                    city['country'] = ""
                    
                try:
                    city['population'] = int(entity.tags['population'])
                except:
                    city['population'] = -1
                    
                try:
                    city['country_code'] = entity.tags['is_in:country_code']
                except:
                    city['country_code'] = ""
                
                try:
                    city['state_code'] = entity.tags['is_in:state_code']
                except:
                    city['state_code'] = ""
                
                try:
                    city['osm_node_id'] = int(entity.id)
                except:
                    city['osm_node_id'] = 0
                
                self.city = self.getCityAndCoutry(city['name'],city['country_code'])
                if self.city == None:
                    self.insertCityInformationOSM(city)
                    self.city = self.getCityAndCoutry(city['name'],city['country_code'])
                else:
                    print 'City realy exist on system'
                    city_exits = True
                    break
                
        if not city_exits:  
            # for all way we create a dict with way's nodes
            city_id = str(self.city.get('_id'))
            for entity in parse_file('data/ex_B5u65rYvSdtoSZj5oZqdqReaVrdsc.osm'):    
                if isinstance(entity, Way) and 'highway' in entity.tags:
                    is_to_insert = False
                    for type_way in self.ways_types:
                        if type_way in entity.tags['highway']:
                            is_to_insert = True

                    if is_to_insert:
                        self.num_total_ways+=1
                        way = {}
                        way['cross_streets_osm_id'] = []
                        way['street_count'] = 0
                        way['busy'] = False
                        way['city_id'] = city_id
                        try:
                            way['name_osm'] = entity.tags['name']
                        except:
                            way['name_osm'] = ""
                            #print 'except name_osm', entity
                        try:
                            way['surface_osm'] = entity.tags['surface']
                        except:
                            None    

                        way['id_osm']      = entity.id
                        #way.city_osm    = 
                        if 'highway' in entity.tags.keys():
                            way['type_osm']    = entity.tags['highway']
                        else:
                            way['type_osm'] = ""
                            #print 'tags->',entity.tags

                        way['nodes'] = []
                        for node in entity.nodes:
                            node = self.nodes[str(node)]
                            lat = node.lat
                            lng = node.lon
                            identifier = node.id
                            highway = None
                            try:
                                highway = node.tags['highway']
                            except:
                                None
                            way['nodes'].append({"lat": lat,"lng": lng,"id": identifier,"highway":highway})
                            #if 'junction' in node.tags or 'highway' in node.tags:
                            #    print 'Junction!', node
                        self.insertStreetInformationOSM(way)
        else:
            print 'None information was inserted or updated'
            
        print 'Total ',self.num_total_ways
    
    
    # insertStreetInformationOSM
    #   insert the strret informatiton
    #   from data collected from osm file
    #
    def insertStreetInformationOSM(self,data):
        self.__collection = self.__db.street
        self.__collection.insert_one(data)
        
    # insertCityInformationOSM
    #   insert the new city from file osm
    #   
    def insertCityInformationOSM(self,data):
        self.__collection = self.__db.city
        self.__collection.insert_one(data)
        
    # getCityAndCoutry
    #   get the informations from city on mongodb
    #
    def getCityAndCoutry(self,name,country_code):
        self.__collection = self.__db.city
        return self.__collection.find_one({'name':name,'country_code':country_code})
        
    def readShapeFromOpenStreet(self,shape_file_url=None):
        if shape_file_url != None:
            self.file_name = shape_file_url
        else:
            self.file_name = self._config.shape_city_url
        
        driver = ogr.GetDriverByName('ESRI Shapefile')
        shp = driver.Open(self._config.shape_city_url)
        layer = shp.GetLayer(0)
        spatialRef = layer.GetSpatialRef()
        print 'spatialRef'
        print spatialRef
        layerDefinition = layer.GetLayerDefn()
        print 'layerDefinition'
        print layerDefinition
        for i in range(50):
            feature = layer.GetFeature(i)
            print feature.ExportToJson()
        