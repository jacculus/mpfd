'''
Created on 19 Jun 2013

@author: Jack
'''

class MPFDMutagenPlugin:
    def __init__(self):
        pass
    
    def getFileMetadata(self, fname):
        return {}
        
    
def createInstance(config):
    return MPFDMutagenPlugin()