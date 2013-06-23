'''
Created on 23 Jun 2013

@author: Jack
'''

import json

class MPFDMetadataTestPlugin:
    def __init__(self):
        pass
    
    def getFileMetadata(self, fname):
        if fname.lower().endswith(".txt"):
            with open(fname, "r") as f:
                t=json.load(f)
                t['filepath']=fname
                return t
        else:
            return None
        
    
def createInstance(config):
    return MPFDMetadataTestPlugin()