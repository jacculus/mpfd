'''
Created on 5 Jun 2013

@author: JSH
'''

import mpfd

class MPFDFilesPlugin:
    def __init__(self, root, mountpoint):
        self.root=root
        self.mountpoint=mountpoint
        self.filePlayerPlugins=None
    
    def getFilePlayers(self):
        self.filePlayerPlugins=[x for x in mpfd.plugins if hasattr(x, "fileFilter")]
                
    def listDir(self, dir):
        if dir.startswith(mountpoint):
            subdir=dir[len(mountpoint):].strip(mpfd.path_separator)
          
        else:
            mpPartitioned=mountpoint.rpartition(mpfd.path_separator)
            if dir.startswith(mpPartitioned[0]):
                return [{'name':mpPartitioned[2], 'type': 'dir'}]

def createInstance(config):
    return MPFDFilesPlugin(config['root'], config['mountpoint'])