from abc import ABC, abstractmethod

class AbstractConfigTemplate(ABC):

    def __init__(self, templateData : any = None):
        pass

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
    def isValidTemplate(templateData : any) -> bool:
        raise NotImplementedError

    

