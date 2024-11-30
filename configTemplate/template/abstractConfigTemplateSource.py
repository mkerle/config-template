from abc import ABC, abstractmethod
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition

from typing import List

class AbstractConfigTemplateSource(ABC):

    def __init__(self, 
                 templateData : any = None):
        
        self.setTemplateData(templateData)

    @abstractmethod
    def setTemplateData(self, templateData : any):
        raise NotImplementedError()

    @abstractmethod
    def getTemplateName(self) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def getTemplateVersion(self) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def isValidTemplate(self) -> bool:
        raise NotImplementedError()
    
    @staticmethod
    @abstractmethod
    def isValidTemplateData(templateData : any) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def getTemplateImports(self) -> List[dict]:
        '''
        Returns a `List` of the inherited templates for the template source.
        Each element of the `List` is a `dict`.
        e.g `[ { 'name' : 'My Template name' } ]`
        '''
        raise NotImplementedError
    
    
    


    

