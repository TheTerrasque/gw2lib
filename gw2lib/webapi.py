import json
import urllib, urllib2
from common import Struct, SimpleCache
import logging
import types

L = logging.getLogger("gw2lib.webapi")

API_CACHE = SimpleCache()

def structify(obj):
    if isinstance(obj, dict):
        return Struct(**obj)
    if isinstance(obj, list):
        return [structify(x) for x in obj]
    return obj


def is_iterable(obj):
    return not isinstance(obj, types.StringTypes) and hasattr( obj, '__iter__')

class SimpleClient(object):
    # http://wiki.guildwars2.com/wiki/API:Main
    
    BASE_URL = "https://api.guildwars2.com/"
    return_struct=True
    
    def _create_kwargs(self, kwargs):
        temp = {}
        for k, v in kwargs.items():
            if is_iterable(v):
                v = ",".join((unicode(x) for x in v))
            temp[k] = v
        return "?" + urllib.urlencode(temp)
    
    def _get_url(self, args, kwargs):
        url = self.BASE_URL + self.version + self.root + (args and "/" + "/".join(unicode(asd) for asd in args) or "")
        if kwargs:
            url = url + self._create_kwargs(kwargs)
        return url
    
    def __init__(self, version="v1", root = "", as_struct = True):
        self.root = root
        self.version = version
        self.return_struct = as_struct

    def dict(self):
        return SimpleClient(version = self.version, root = self.root, as_struct=False)
        
    def __getattr__(self, attrib):
        return SimpleClient(version = self.version, root = self.root + "/" + attrib, as_struct=self.return_struct)
    
    def get_help_url(self):
        """
        Guesstimates the gw2 wiki help page for this API endpoint
        """
        url = self._get_url([], {})
        url = url.replace(self.BASE_URL + "v", "http://wiki.guildwars2.com/wiki/API:")
        return url
    
    def _fetch_url(self, url):
        return urllib2.urlopen(url).read()
        
    def __call__(self, *args, **kwargs):
        url = self._get_url(args, kwargs)
        L.debug("URL: %s", url)
        
        d = API_CACHE.get(url)
        if d == None:
            d = self._fetch_url(url)
            API_CACHE.set(url, d)
            
        r = json.loads(d)
        
        if self.return_struct:
            r = structify(r)
        return r