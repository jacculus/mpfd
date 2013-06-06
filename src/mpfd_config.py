'''
Created on 5 Jun 2013

@author: JSH
'''

import mpfd
from mpfd_log import log
import ConfigParser
import importlib

def loadConfig(configFile):
    config=ConfigParser.ConfigParser()
    config.read(configFile)
    
    #Load plugins
    for section in config.sections():
        plugin=config.get(section, 'plugin')
        if plugin==None:
            log("WARNING: Section {}: no plugin specified, skipping".format(section))
            continue
        pluginModule=importlib.import_module(plugin)
        pluginInstance=pluginModule.createInstance(dict(x for x in config.items(section) if x[0]!='plugin'))
        mpfd.plugins.append(pluginInstance)