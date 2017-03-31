#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import pymongo
from pymongo import MongoClient
from osgeo import ogr, osr
from osmread import parse_file, Way, Node,Relation

from Configuration import Configuration
class Reader:
    
    
    _config      = None
    file_name   = None
    nodes       = None
    
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
               
          
        # for all way we create a dict with way's nodes
        for entity in parse_file('data/ex_B5u65rYvSdtoSZj5oZqdqReaVrdsc.osm'):    
            if isinstance(entity, Way) and 'highway' in entity.tags:
                is_to_insert = False
                for type_way in self.ways_types:
                    if type_way in entity.tags['highway']:
                        is_to_insert = True
                        
                if is_to_insert:
                    way = {}
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
                #if not is_to_insert:
                    #print 'Node',entity.tags
            
            
            #if isinstance(entity, Way) in entity:
            #    way_count += 1
            #    if way_count == 1:
            #        print '\nWay ->', entity
            #if isinstance(entity, Way) and 'oneway' in entity.tags and entity.tags['highway'] == 'residential':
            #    oneway_count += 1
            #   if oneway_count == 1:
            #        print '\nWay Oneway ->', entity
            #if isinstance(entity, Way) and 'junction' in entity.tags and entity.tags['junction'] == 'yes':
            #    junction_count += 1
                #if junction_count == 1:
            #    print '\nWay Junction ->', entity
            #if isinstance(entity, Way) and 'highway' in entity.tags and 'junction' in entity.tags:
            #    junction_node_count += 1
            #    if junction_node_count == 1:
            #        print '\nWay Junction 1 ->', entity
            #    if junction_node_count == 10:
            #        print '\nWay Junction 2 ->', entity
            #
            #if isinstance(entity, Way) and 'highway' in entity.tags:
            #    highway_count += 1
            #    if highway_count == 1:
            #        print '\nHighway ->', entity
            #if isinstance(entity, Way) and 'barrier' in entity.tags:
            #    barrier_count += 1
            #    if barrier_count == 1:
            #        print '\nBarrier ->', entity
            #if isinstance(entity, Way) and 'highway' in entity.tags and entity.tags['highway'] == 'cycleway':
            #    cycleway_count += 1
            #    if cycleway_count == 1:
            #        print '\nCycleway ->', entity
            #        
            #if isinstance(entity,Node) in entity:
            #    node_count +=1
            #    if node_count == 1:
            #        print '\nNode -> ', entity
            #        
            #if isinstance(entity,Relation) in entity:
            #    relation_count +=1
            #    if relation_count == 1:
            #        print '\nRelation Node -> ', entity
            #    #print("%d highways found" % highway_count)
        print 'Total ',self.num_total_ways
    # updateUserInformation
    #
    def insertStreetInformationOSM(self,data):
        self.__collection = self.__db.street
        self.__collection.insert_one(data)
        
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
        