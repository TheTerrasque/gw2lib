import logging
import cPickle as pickle
from datetime import datetime, timedelta

from base64 import b64encode
def genItemChatCode(item_id, item_count=1, itemtype=2):
    """
    Generate a chat code for an item ID.
    
    Credit: https://forum-en.guildwars2.com/forum/community/api/How-to-Get-chat-code-with-item-ID
    """
    hexa = chr(itemtype) + chr(item_count) # Item type, number
    for i in range(4):
        hexa += chr(item_id % 256)
        item_id //= 256
    return '[&' + b64encode(hexa).decode(encoding="UTF-8") + ']'

class Struct:
    """
    Dictionary helper class
    """
    __level = 1
    
    def __init__(self, STRUCT_LEVEL=1, **entries):
        for k, v in entries.iteritems():
            if isinstance(v, dict):
                entries[k] = Struct(STRUCT_LEVEL+1, **v)
        self.__level = STRUCT_LEVEL
        self.__dict__.update(entries)
    
    def __repr__(self):
        spc = " " * self.__level * 2
        return '[Structure]\n' + spc + '%s' % str(('\n' + spc).join('%s : %s' % (k, repr(v)) for (k, v) in self.__dict__.iteritems() if k[0] != "_")) 

L = logging.getLogger("gw2lib.simplecache")

class SimpleCache(object):
    """
    Very simple key -> value cache that resets the cache at *length* number of entries,
    and also invalidates entries after *age* time has passed.
    """
    
    oldest = None
    
    def __init__(self, length=512, age = 60*60*24):
        self.length = length
        self.cache = {}
        self.oldest = datetime.now()
        self.delta = timedelta(seconds = age)
    
    def load(self, filename="webcache.p"):
        try:
            with open(filename, "r") as f:
                self.cache = pickle.load(f)
                self.oldest = datetime(1990, 01, 01)
        except IOError:
            pass
    
    def save(self, filename="webcache.p"):
        with open(filename, "w") as f:
            pickle.dump(self.cache, f)
    
    def set(self, key, value):
        self.check_length()
        self.cache[key] = {"value":value, "time":datetime.now()}

    def get(self, key):
        v = self.cache.get(key)
        if v and (datetime.now() - v["time"] < self.delta):
            return v["value"]

    def check_length(self):
        old_mark = datetime.now() - self.delta
        
        if self.oldest < old_mark:
            c = {}
            self.oldest = datetime.now()
            
            for k, v in self.cache.iteritems():
                if v["time"] < old_mark:
                    c[k] = v
                    if self.oldest > v["time"]:
                        self.oldest = v["time"]
            self.cache = c
            
        if len(self.cache) > self.length:
            L.debug("Culled cache")
            self.cache = {} # not ideal, but beats it growing forever