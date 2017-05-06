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
        db.crawler_image.delete_many({})
        db.crawler_session.delete_many({})
        os.chdir('../crawler/data/flickr/')
        filelist = [ f for f in os.listdir(".") if f.endswith(".jpg") ]
        for f in filelist:
            os.remove(f)
        
    if '-r' in commands:
        db.city.delete_many({})
        db.street.delete_many({})
        os.chdir('../read_osm/data/')
        