'''
Created on 9 Jun 2013

@author: Jack
'''
import subprocess

class MPFDMPlayerPlugin:
    def __init__(self):
        self.mpProcess=None
    
    def fileFilter(self, name):
        if name.endswith(".mp3"):
            return name.rpartition(".")[0]
        return None
    
    def canPlayLocalFile(self, fpath):
        return fpath.lower().endswith(".mp3")
    
    def playLocalFile(self, fpath):
        if self.mpProcess and self.mpProcess.poll()==None:
            self.mpProcess.kill()
            self.mpProcess=None
        self.mpProcess=subprocess.Popen(['mplayer',fpath])
        return True
    
    def stop(self):
        if self.mpProcess and self.mpProcess.poll()==None:
            self.mpProcess.kill()
            self.mpProcess=None
    
def createInstance(config):
    return MPFDMPlayerPlugin()