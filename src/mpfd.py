'''
Created on 5 Jun 2013

@author: JSH
'''

path_separator='/'
plugins=[]

def listDir(dirname):
    listing=[]
    for plugin in plugins:
        if hasattr(plugin, "listDir"):
            returnedFromPlugin=plugin.listDir(dirname)
            if returnedFromPlugin!=None:
                listing.extend(returnedFromPlugin)
    return listing