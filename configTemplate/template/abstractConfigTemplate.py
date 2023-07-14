from abc import ABC, abstractmethod

class AbstractConfigTemplate(ABC):

    def __init__(self, templateData : any = None):
        
        self._templateVariablePrefix = '$_var_'
        self._variableStart = '{{'
        self._variableEnd = '}}'

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
    
    def setTemplateVariablePrefix(self, templateVariablePrefix : str):
        self._templateVariablePrefix = templateVariablePrefix

    def getTemplateVariablePrefix(self) -> str:
        return self._templateVariablePrefix

    def setVariableStart(self, variableStart : str):
        self._variableStart = variableStart

    def getVariableStart(self) -> str:
        return self._variableStart

    def setVariableEnd(self, variableEnd : str):
        self._variableEnd = variableEnd

    def getVariableEnd(self) -> str:
        return self._variableEnd


    

