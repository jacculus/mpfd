'''
Created on 5 Jun 2013

@author: JSH
'''

import mpfd
import os

class MPFDFilesMountpoint:
    def __init__(self, mp, mpType):
        self.mp=mp
        self.mpType=mpType
        
    def isDirectory(self):
        return 'directory' in self.mpType
        
class MPFDFilesPlugin:
    def __init__(self, root, mountpoints):
        self.root=root
        self.mountpoints=mountpoints
        self.filePlayerPlugins=None
    
    def getFilePlayers(self):
        self.filePlayerPlugins=[x for x in mpfd.plugins if hasattr(x, "fileFilter")]
    
    def listDirectoryMountpoint(self, subdir):
        path=os.path.join(self.root,subdir)
        entries=os.listdir(path)
        result=[]
        for entry in entries:
            if os.path.isdir(os.path.join(path,entry)):
                result.insert(0,{'name':entry, 'type': 'dir'})
            else:
                for plugin in self.filePlayerPlugins:
                    realname=plugin.fileFilter(entry)
                    if realname!=None:
                        result.append({'name':entry, 'realname': realname, 'type': 'file'})
                        break
        return result
    
    def listMetadataMountpoint(self, mountpoint, subdir):
        return [{ 'name': 'test', 'realname': 'test', 'type': 'file'}]
    
    def listDir(self, dirname):
        if self.filePlayerPlugins==None:
            self.getFilePlayers()
        result=[]
        for mountpoint in self.mountpoints:
            if dirname.startswith(mountpoint.mp):            
                subdir=dirname[len(mountpoint.mp):].strip(mpfd.path_separator)
                if mountpoint.isDirectory():
                    result.extend(self.listDirectoryMountpoint(subdir))
                else:
                    result.extend(self.listMetadataMountpoint(mountpoint,subdir))
            else:
                mpPartitioned=mountpoint.mp.rpartition(mpfd.path_separator)
                if dirname.rstrip(mpfd.path_separator)==mpPartitioned[0]:
                    result.append({'name':mpPartitioned[2], 'type': 'dir'})
        return result

mpTypes=[ 'directory', 'album', 'artist' ]
def extractMountpoint(mpStr):
    cparts=mpStr.split(',')
    mpType=[]
    while cparts[-1] in mpTypes:
        mpType.insert(0,cparts.pop())
    return MPFDFilesMountpoint(','.join(cparts),mpType)
        
def createInstance(config):
    return MPFDFilesPlugin(config['root'], [extractMountpoint(config[x]) for x in config if x.startswith("mountpoint")])