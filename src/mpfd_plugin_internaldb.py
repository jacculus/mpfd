'''
Created on 20 Jun 2013

@author: Jack
'''

import threading
import pickle
import os

class MPFDInternalDatabaseAutosaveThread(threading.Thread):
    def __init__(self, plugin):
        super(MPFDInternalDatabaseAutosaveThread, self).__init__()
        self.plugin=plugin
        self.daemon=True
        self.cv=threading.Condition()
        self.stopping=False
    
    def stop(self):
        self.stopping=True
        self.cv.acquire()
        self.cv.notifyAll()
        self.cv.release()
        
    def run(self):
        while not self.stopping:
            self.cv.acquire()
            self.cv.wait(60)
            self.cv.release()
            if self.plugin.changedSinceLastSave():
                self.plugin.save()
    
class MPFDInternalDatabasePlugin:
    def __init__(self, savefile):
        self.data={}
        self.savefile=savefile
        self.changed=False
    
    def storeDB(self, name, obj):
        self.data[name]=obj
        self.changed=True
    
    def getDB(self, name, default=None):
        if name in self.data:
            return self.data[name]
        elif default==None:
            return None
        else:
            self.data[name]=default
            self.changed=True
            return default
    
    def start(self):
        self.load()
        self.autosaveThread=MPFDInternalDatabaseAutosaveThread(self)
        self.autosaveThread.start()
        
    def stop(self):
        self.autosaveThread.stop()
    
    def changedSinceLastSave(self):
        #TODO: doesn't notify of changes in tables
        return self.changed
    
    def save(self):
        with open(self.savefile,"wb") as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
            
    def load(self):
        if os.path.exists(self.savefile):
            with open(self.savefile,"rb") as f:
                self.data=pickle.load(f)
            
def createInstance(config):
    return MPFDInternalDatabasePlugin(config['file'] if 'file' in config else '.mpfd_internaldb')