from abc import ABC, classmethod, abstractmethod

class AbstractConfigTemplate(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def getTemplateName(self) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def getTemplateVersion(self) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def isValidTemplate(self) -> bool:
        raise NotImplementedError()

    

