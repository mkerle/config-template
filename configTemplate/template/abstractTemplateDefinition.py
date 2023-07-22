from abc import ABC, abstractmethod

class AbstractTemplateDefinition(ABC):

    def __init__(self):

        self._templateVariablePrefix = '$_var_'
        self._importBlocks = '$_import_blocks'
        self._variableStart = '{{'
        self._variableEnd = '}}'

    def setTemplateVariablePrefix(self, templateVariablePrefix : str):
        self._templateVariablePrefix = templateVariablePrefix

    def getTemplateVariablePrefix(self) -> str:
        return self._templateVariablePrefix
    
    def setImportBlockVariableName(self, importBlocksVariable : str):
        self._importBlocks = importBlocksVariable

    def getImportBlockVariableName(self) -> str:
        return self._importBlocks

    def setVariableStart(self, variableStart : str):
        self._variableStart = variableStart

    def getVariableStart(self) -> str:
        return self._variableStart

    def setVariableEnd(self, variableEnd : str):
        self._variableEnd = variableEnd

    def getVariableEnd(self) -> str:
        return self._variableEnd
    
    def isTemplateKeyword(self, s : str) -> bool:

        if (s.startswith(self.getTemplateVariablePrefix())):
            return True
        
        if (s == self.getImportBlockVariableName()):
            return True
        
        return False
    
    def hasTemplateVariable(self, s : str) -> bool:

        return s.strip().startswith(self.getVariableStart()) and s.strip().endswith(self.getVariableEnd())