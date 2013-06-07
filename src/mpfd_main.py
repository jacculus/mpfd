'''
Created on 5 Jun 2013

@author: JSH
'''

import mpfd
import mpfd_config
import mpfd_socket

import socket

mpfd_config.loadConfig(".mpfd")

serverSocketThread=mpfd_socket.ServerSocketThread()
serverSocketThread.start()

print "Config loaded"
print mpfd.plugins