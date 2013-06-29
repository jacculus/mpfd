'''
Created on 19 Jun 2013

@author: Jack
'''

from mutagen.id3 import ID3
from mutagen.id3 import ID3NoHeaderError

class MPFDMutagenPlugin:
    def __init__(self):
        pass
    
    def getFileMetadata(self, fname):
        try:
            idtag=ID3(fname)
            return {'filepath':fname,
                     'artist':idtag['TPE1'].text[0] if 'TPE1' in idtag else '',
                     'album':idtag['TALB'].text[0] if 'TALB' in idtag else '',
                     'title':idtag['TIT2'].text[0] if 'TIT2' in idtag else ''
                   }
        except ID3NoHeaderError:
            return None
    
def createInstance(config):
    return MPFDMutagenPlugin()