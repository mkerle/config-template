from abc import ABC, classmethod, abstractmethod

from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate
from configTemplate.importSource.abstractTemplateSourceCache import AbstractTemplateSourceCache

class AbstractTemplateImportSource(ABC):

    def __init__(self):
        
        self.importSourceCache = AbstractTemplateSourceCache()

    def clearCache(self):
        self.importSourceCache.clearCache()

    @abstractmethod
    def buildCache(self):
        raise NotImplementedError()

    @abstractmethod
    def hasTemplate(self, templateName : str, version : int) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def getTemplate(self, templateName : str, version : int) -> AbstractConfigTemplate:
        raise NotImplementedError()