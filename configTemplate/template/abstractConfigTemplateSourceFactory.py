from abc import ABC, abstractmethod

from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource

class AbstractConfigTemplateSourceFactory(ABC):

    @staticmethod
    @abstractmethod    
    def createTemplateSource(*args, **kwargs) -> AbstractConfigTemplateSource:
        raise NotImplementedError()
    