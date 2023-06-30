from abc import ABC, classmethod, abstractmethod

from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate

class AbstractTemplateSourceCache(ABC):

    def __init__(self):

        self.cache = {}

    def clearCache(self):
        self.cache = {}

    @abstractmethod
    def _getCacheKey(self, templateName : str, templateVersion : int) -> str:

        raise NotImplementedError()

    @abstractmethod
    def add(self, templateName : str, templateVersion : int, obj : any = None):

        raise NotImplementedError()
    
    @abstractmethod
    def get(self, templateName : str, templateVersion : int) -> AbstractConfigTemplate:

        raise NotImplementedError()
