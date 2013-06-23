'''
Created on 5 Jun 2013

@author: JSH
'''

import mpfd
import mpfd_config
import threading
import time
import atexit

startedPlugins=[]

def exitHandler():
    for plugin in startedPlugins:
        if hasattr(plugin, 'stop'):
            plugin.stop()
            
mpfd_config.loadConfig(".mpfd")

atexit.register(exitHandler)

for plugin in mpfd.plugins:
    if hasattr(plugin, 'start'):
        plugin.start()
        startedPlugins.append(plugin)

print "Config loaded"
print mpfd.plugins

while threading.active_count()>0:
    time.sleep(0.1)
    
