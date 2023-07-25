from abc import ABC, abstractmethod

class AbstractTemplateDefinition(ABC):

    def __init__(self):

        self._templateVariablePrefix = '$_var_'
        self._importBlocks = '$_import_blocks'
        self._variableStart = '{{'
        self._variableEnd = '}}'
        self._logicStart = '{%'
        self._logicEnd = '%}'

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
    
    def setLogicStart(self, logicStart : str):
        self._logicStart = logicStart

    def getLogicStart(self) -> str:
        return self._logicStart
    
    def setLogicEnd(self, logicEnd : str):
        self._logicEnd = logicEnd
    
    def getLogicEnd(self) -> str:
        return self._logicEnd
    
    def isTemplateKeyword(self, s : str) -> bool:

        if (s.startswith(self.getTemplateVariablePrefix())):
            return True
        
        if (s == self.getImportBlockVariableName()):
            return True
        
        return False
    
    def hasTemplateVariable(self, s : str) -> bool:

        if (type(s) == str):
            return s.strip().startswith(self.getVariableStart()) and s.strip().endswith(self.getVariableEnd())
        
        return False
    
    def hasTemplateLogic(self, s : str) -> bool:

        if (type(s) == str):
            return s.strip().startswith(self.getLogicStart()) and s.strip().endswith(self.getLogicEnd())
        
        return False
    
    def _getLogicParts(self, s : str) -> dict:

        logic = {'condition' : None, 'true' : None, 'else' : None }

        if (type(s) == str and ' if ' in s and ' then ' in s):

            logic['condition'] = s.split(' then ')[0].split(' if ')[1].strip()

            returnPart = s.split(' then ')[1].replace(self.getLogicEnd(), '').strip()
            if (' else ' in s):
                logic['true'] = returnPart.split(' else ')[0].strip()
                logic['else'] = returnPart.split(' else ')[1].strip()
            else:
                logic['true'] = returnPart

        else:
            raise Exception('Invalid logic statement: "%s"' % (s))
        
        return logic


    def getLogicCondition(self, s : str) -> str:

        return self._getLogicParts(s)['condition']
    
    def _getLogicReturnValue(self, valStr : str) -> any:

        valStr = valStr.strip()
        if (self.hasTemplateVariable(valStr)):
            return valStr
        elif (valStr.startswith('{') and valStr.endswith('}')):
            return eval(valStr)
        elif (valStr.startswith('[') and valStr.endswith(']')):
            return eval(valStr)
        elif (valStr.startswith("'") and valStr.endswith("'")):
            return valStr
        elif (valStr.isnumeric()):
            return int(valStr)
        
        raise Exception('Unable to determine logic return value type for: %s' % (valStr))

    def getLogicReturnTrue(self, s : str) -> any:

        return self._getLogicReturnValue(self._getLogicParts(s)['true'])
    
    def getLogicReturnFalse(self, s : str) -> any:

        return self._getLogicReturnValue(self._getLogicParts(s)['else'])
