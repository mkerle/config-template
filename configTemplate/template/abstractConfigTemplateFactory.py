from abc import ABC, abstractmethod

from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate

class AbstractConfigTemplateFactory(ABC):

    @staticmethod
    @abstractmethod    
    def createTemplate(*args, **kwargs) -> AbstractConfigTemplate:
        raise NotImplementedError()
    