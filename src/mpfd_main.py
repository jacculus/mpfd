'''
Created on 5 Jun 2013

@author: JSH
'''

import mpfd
import mpfd_config
import mpfd_socket
import threading
import time

mpfd_config.loadConfig(".mpfd")

serverSocketThread=mpfd_socket.ServerSocketThread()
serverSocketThread.start()

print "Config loaded"
print mpfd.plugins

while threading.active_count()>0:
    time.sleep(0.1)