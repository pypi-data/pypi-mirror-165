import os
import time

from os.path import *

class Cache(object):
    def __init__(self, load=None):
        self.cache = {}
        if load is not None:
            self.load = load

    def get(self, key, *loadargs):
        obj = self.cache.get(key)
        nobj = self.load(key, obj, *loadargs)
        if nobj is not obj:
            if hasattr(obj, 'close'):
                obj.close()
            if nobj is None:
                try:
                    del self.cache[key]
                except KeyError:
                    pass
            else:
                self.cache[key] = nobj

        return nobj

    def load(self, key, obj):
        pass

class FileCache(Cache):
    def __init__(self, loadfile=None):
        Cache.__init__(self)
        if loadfile is not None:
            self.loadfile = loadfile

    def load(self, key, obj, stat=None):
        cachemtime = None
        if obj is not None:
            cachemtime = obj.stat.st_mtime

        if stat is None:
            try:
                stat = os.stat(key)
            except Exception:
                return

        if cachemtime is None or stat.st_mtime > cachemtime:
            return self.loadfile(key, stat)
        return obj

    def loadfile(self, path, stat):
        pass
