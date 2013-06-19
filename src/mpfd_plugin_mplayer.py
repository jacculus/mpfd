'''
Created on 9 Jun 2013

@author: Jack
'''

class MPFDMPlayerPlugin:
    def __init__(self):
        pass
    
    def fileFilter(self, name):
        if name.endswith(".mp3"):
            return name.rpartition(".")[0]
        return None
        
    
def createInstance(config):
    return MPFDMPlayerPlugin()