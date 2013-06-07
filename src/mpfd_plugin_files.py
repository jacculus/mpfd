'''
Created on 5 Jun 2013

@author: JSH
'''

import mpfd
import os

class MPFDFilesPlugin:
    def __init__(self, root, mountpoint):
        self.root=root
        self.mountpoint=mountpoint
        self.filePlayerPlugins=None
    
    def getFilePlayers(self):
        self.filePlayerPlugins=[x for x in mpfd.plugins if hasattr(x, "fileFilter")]
                
    def listDir(self, dir):
		if self.filePlayerPlugins==None:
			getFilePlayers()
        if dir.startswith(mountpoint):
            subdir=dir[len(mountpoint):].strip(mpfd.path_separator)
			path=os.path.join(root,subdir)
			entries=os.listdir(path)
			result=[]
			for entry in entries:
				if os.path.isdir(os.path.join(path,entry)):
					result.insert(0,{'name':entry, 'type': 'dir'})
				else:
					for plugin in self.filePlayerPlugins:
						realname=plugin.fileFilter(entry)
						if realname!=None:
							result.append({'name':entry, 'realname': realname, 'type': 'file', 'player':plugin})
							break
				
        else:
            mpPartitioned=mountpoint.rpartition(mpfd.path_separator)
            if dir.startswith(mpPartitioned[0]):
                return [{'name':mpPartitioned[2], 'type': 'dir'}]

def createInstance(config):
    return MPFDFilesPlugin(config['root'], config['mountpoint'])