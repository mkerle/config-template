from abc import ABC, abstractmethod

import logging

class AbstractTemplateSourceCache(ABC):

    def __init__(self):

        self.cache = {}

    def clearCache(self):

        logging.debug('AbstractTemplateSourceCache.clearCache() -> Clearing cache')

        self.cache = {}

    def add(self, k : str, obj : any = None):

        logging.debug('AbstractTemplateSourceCache.add() -> Adding key [%s] with value %s to cache' % (k, str(obj)))

        self.cache[k] = obj
    
    def get(self, k : str) -> any:

        logging.debug('AbstractTemplateSourceCache.get() -> Checking cache for key [%s]' % (k))

        if (k in self.cache):
            return self.cache[k]
    
        return self.cache.get(k, None)

