#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, pymongo
from pymongo import MongoClient

if __name__ == "__main__":
    
    
    commands = sys.argv[1:len(sys.argv)]
    for i in range(len(commands)):
        commands[i] = commands[i].lower()
    
    client		= MongoClient('localhost', 27017)
    db			= client['graphium']
    
    if '-c' in commands:
        print 'Removing Crawler data'
        print 'Crawler_image total', db.crawler_image.count({})
        print 'crawler_session total', db.crawler_session.count({})
        db.crawler_image.delete_many({})
        db.crawler_session.delete_many({})
        os.chdir('../crawler/data/flickr/')
        filelist = [ f for f in os.listdir(".") if f.endswith(".jpg") ]
        print 'Images at data folder',len(filelist)
        for f in filelist:
            os.remove(f)
        
    if '-r' in commands:
        print 'Removing OSM data'
        print 'City total', db.city.count({})
        print 'Street total', db.street.count({})
        db.city.delete_many({})
        db.street.delete_many({})
        
    if '-s' in commands:
        print 'Removing Sessions Swarm data'
        print 'Swarms total', db.swarm.count({})
        print 'Agents total', db.agent.count({})
        db.swarm.delete_many({})
        db.agent.delete_many({})