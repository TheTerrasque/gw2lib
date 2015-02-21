import json
import urllib, urllib2
from common import Struct, SimpleCache
import logging

L = logging.getLogger("gw2lib.webapi")

API_CACHE = SimpleCache()

class SimpleAPIClient(object):
    # http://wiki.guildwars2.com/wiki/API:Main
    
    BASE_URL = "https://api.guildwars2.com/"
    
    def _get_url(self, args, kwargs):
        url = self.BASE_URL + self.version + self.root + (args and "/" + "/".join(unicode(asd) for asd in args) or "")
        
        if kwargs:
            url = url + "?" + urllib.urlencode(kwargs)
            
        return url
    
    def __init__(self, version="v1", root = ""):
        self.root = root
        self.version = version

    def __getattr__(self, attrib):
        return SimpleAPIClient(version = self.version, root = self.root + "/" + attrib)
    
    def get_help_url(self):
        url = self._get_url([], {})
        url = url.replace(self.BASE_URL + "v", "http://wiki.guildwars2.com/wiki/API:")
        return url
        
    def __call__(self, *args, **kwargs):
        url = self._get_url(args, kwargs)
        L.debug("URL: %s", url)
        
        r = API_CACHE.get(url)
        if r == None:
            d = urllib2.urlopen(url).read()
            r = json.loads(d)
            if isinstance(r, dict):
                r = Struct(**r)
            API_CACHE.set(url, r)
        return r