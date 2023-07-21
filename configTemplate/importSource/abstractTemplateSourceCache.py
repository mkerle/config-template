from abc import ABC, abstractmethod

class AbstractTemplateSourceCache(ABC):

    def __init__(self):

        self.cache = {}

    def clearCache(self):
        self.cache = {}

    def add(self, k : str, obj : any = None):

        self.cache[k] = obj
    
    def get(self, k : str) -> any:
    
        return self.cache.get(k, None)

