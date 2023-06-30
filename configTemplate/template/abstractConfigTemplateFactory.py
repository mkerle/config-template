from abc import abc, classmethod, abstractmethod

from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate

class AbstractConfigTemplateFactory(abc):

    @abstractmethod
    def createTemplateFromObject(obj : any) -> AbstractConfigTemplate:
        raise NotImplementedError()
    
    @abstractmethod
    def createTemplateFromFile(filePath : str) -> AbstractConfigTemplate:
        raise NotImplementedError()