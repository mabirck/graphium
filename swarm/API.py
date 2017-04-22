from osmapi import OsmApi

class API:
    
    _instance   = None
    _my_api     = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(API, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self._my_api = OsmApi(username = u"glaucomunsberg", password = u"********")
        print 'API'
        #print self._my_api.NodeGet(123)
        
    def getWaysByNode(self,NodeId):
        #print 'getWaysByNode... ',NodeId
        results = self._my_api.NodeWays(int(NodeId))
        to_return = []
        
        for result in results:
            #print 'result: ',result
            the_way = {}
            the_way['id'] = result['id']
            the_way['nodes'] = []
            if 'tag' in result.keys():
                #print 'tags: ', result['tag']
                if 'name' in result['tag'].keys():
                    the_way['name'] = result['tag']['name']
                else:
                    the_way['name'] = None
                
            if 'nd' in result.keys():
                #print 'nodes: ',result['nd']
                the_way['nodes'] = result['nd']
            to_return.append(the_way)
        return to_return
        