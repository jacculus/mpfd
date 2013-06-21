'''
Created on 20 Jun 2013

@author: Jack
'''

import threading
import pickle
import os

class MPFDInternalDatabaseAutosaveThread(threading.Thread):
    def __init__(self, plugin):
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
    
    def storeDB(self, name, obj):
        self.data[name]=obj
    
    def getDB(self, name, default=None):
        if name in self.data:
            return self.data[name]
        elif default==None:
            return None
        else:
            self.data[name]=default
            return default
    
    def start(self):
        self.load()
        self.autosaveThread=MPFDInternalDatabaseAutosaveThread(self)
        self.autosaveThread.start()
        
    def stop(self):
        self.autosaveThread.stop()
        
    def save(self):
        with open(self.savefile,"wb") as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
            
    def load(self):
        if os.path.exists(self.savefile):
            with open(self.savefile,"rb") as f:
                self.data=pickle.load(f)
            
def createInstance(config):
    return MPFDInternalDatabasePlugin()