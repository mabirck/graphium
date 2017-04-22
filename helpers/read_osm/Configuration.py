#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Configuration:
    
    _instance               = None
    shape_city_url          = "data/ex_B5u65rYvSdtoSZj5oZqdqReaVrdsc_osm_roads.shp"     # shape IMPOSM
    osm_city_url            = "data/ex_B5u65rYvSdtoSZj5oZqdqReaVrdsc.osm"               #OSM XML
    
    
    # OSM Configuration
    use_urban_ways          = True
    use_motorways           = True
    use_othersways          = False
    
    urban_highway_tipes         = ["tertiary", "road", "residential", "service", "living_street", "pedestrian", "bus_guideway", "steps","secondary", "trunk", "primary"]
    motorways_highway_tipes     = ["motorway", "escape"]
    others_highway_tipes        = ["track"]
    
    
    # MongoDB
    mongo_db            = "graphium"    # databse default
    mongo_host          = "localhost"   # host of mongodb
    mongo_port          = 27017         # port of mongodb
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance

	def __init__(self):
        
		print 'Config load' 