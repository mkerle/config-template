from abc import ABC, abstractmethod

from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource
from configTemplate.importSource.abstractTemplateSourceCache import AbstractTemplateSourceCache
from configTemplate.template.abstractConfigTemplateSourceFactory import AbstractConfigTemplateSourceFactory

class AbstractTemplateImportSource(ABC):

    def __init__(self, directoryPath : str, factoryMethod : AbstractConfigTemplateSourceFactory):
        
        self.directoryPath = directoryPath
        self.factoryMethod = factoryMethod

    def clearCache(self):
        self.importSourceCache.clearCache()

    @abstractmethod
    def buildCache(self):
        raise NotImplementedError()
    
    @abstractmethod
    def refreshCache(self):
        raise NotImplementedError()

    @abstractmethod
    def hasTemplate(self, *args, **kwargs) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def getTemplate(self, *args, **kwargs) -> AbstractConfigTemplateSource:
        raise NotImplementedError()