from abc import ABC, abstractmethod

import re

class AbstractTemplateDefinition(ABC):

    CONTROL_STRUCTURE_TYPE_IF = 'if'
    CONTROL_STRUCTURE_TYPE_FOR = 'for'

    CONTROL_STRUCTURE_REGEX_IF = r'{%\s+if\s+(.*?)\s+then\s+(.*?)(?=else)(else)?(.*)%}|{%\s+if\s+(.*?)\s+then\s+(.*?)%}'
    CONTROL_STRUCTURE_REGEX_FOR = r'{%\s+for\s+(.*?)\s+in\s+(.*?)\s+do\s+(.*)%}'

    CONTROL_STRUCTURE_DATASRC_FOR = 'dataSrc'
    CONTROL_STRUCTURE_RETVAL_FOR = 'retVals'

    def __init__(self):

        self._templateVariablePrefix = '$_var_'
        self._importBlocks = '$_import_blocks'
        self._appendToList = '$_append_to_list'
        self._variableStart = '{{'
        self._variableEnd = '}}'
        self._controlStructureStart = '{%'
        self._controlStructureEnd = '%}'

    def setTemplateVariablePrefix(self, templateVariablePrefix : str):
        self._templateVariablePrefix = templateVariablePrefix

    def getTemplateVariablePrefix(self) -> str:
        return self._templateVariablePrefix
    
    def setImportBlockVariableName(self, importBlocksVariable : str):
        self._importBlocks = importBlocksVariable

    def getImportBlockVariableName(self) -> str:
        return self._importBlocks
    
    def setAppendToListVariableName(self, appendToListVariable : str):
        self._appendToList = appendToListVariable

    def getAppendToListVariableName(self) -> str:
        return self._appendToList

    def setVariableStart(self, variableStart : str):
        self._variableStart = variableStart

    def getVariableStart(self) -> str:
        return self._variableStart

    def setVariableEnd(self, variableEnd : str):
        self._variableEnd = variableEnd

    def getVariableEnd(self) -> str:
        return self._variableEnd
    
    def setControlStructureStart(self, controlStructureStart : str):
        self._controlStructureStart = controlStructureStart

    def getControlStructureStart(self) -> str:
        return self._controlStructureStart
    
    def setControlStructureEnd(self, controlStructureEnd : str):
        self._controlStructureEnd = controlStructureEnd
    
    def getControlStructureEnd(self) -> str:
        return self._controlStructureEnd
    
    def isTemplateKeyword(self, s : str) -> bool:

        if (s.startswith(self.getTemplateVariablePrefix())):
            return True
        
        if (s == self.getImportBlockVariableName()):
            return True
        
        if (s == self.getAppendToListVariableName()):
            return True
        
        return False
    
    def hasTemplateVariable(self, s : str) -> bool:

        if (type(s) == str):
            return s.strip().startswith(self.getVariableStart()) and s.strip().endswith(self.getVariableEnd())
        
        return False
    
    def hasTemplateControlStructure(self, s : str) -> bool:

        if (type(s) == str):
            return s.strip().startswith(self.getControlStructureStart()) and s.strip().endswith(self.getControlStructureEnd())
        
        return False
    
    def getTypeOfControlStructure(self, s : str) -> str | None:

        if (re.match(self.CONTROL_STRUCTURE_REGEX_IF, s)):
            return self.CONTROL_STRUCTURE_TYPE_IF
        
        if (re.match(self.CONTROL_STRUCTURE_REGEX_FOR, s)):
            return self.CONTROL_STRUCTURE_TYPE_FOR
        
        return None
    
    def _getIfControlStructureParts(self, s : str) -> dict:

        logic = {'condition' : None, 'true' : None, 'else' : None }

        if (type(s) == str and ' if ' in s and ' then ' in s):

            logic['condition'] = s.split(' then ')[0].split(' if ')[1].strip()

            returnPart = s.split(' then ')[1].replace(self.getControlStructureEnd(), '').strip()
            if (' else ' in s):
                logic['true'] = returnPart.split(' else ')[0].strip()
                logic['else'] = returnPart.split(' else ')[1].strip()
            else:
                logic['true'] = returnPart

        else:
            raise Exception('Invalid logic statement: "%s"' % (s))
        
        return logic


    def getIfControlStructureCondition(self, s : str) -> str:

        return self._getIfControlStructureParts(s)['condition']
    
    def _getIfControlStructureReturnValue(self, valStr : str) -> any:

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

    def getIfControlStructureReturnTrue(self, s : str) -> any:

        return self._getIfControlStructureReturnValue(self._getIfControlStructureParts(s)['true'])
    
    def getIfControlStructureReturnFalse(self, s : str) -> any:

        return self._getIfControlStructureReturnValue(self._getIfControlStructureParts(s)['else'])
    
    def getForControlStructureCode(self, s : str) -> (str, str):

        if (self.getTypeOfControlStructure(s) == self.CONTROL_STRUCTURE_TYPE_FOR):
            
            try:
                match = re.match(self.CONTROL_STRUCTURE_REGEX_FOR, s)

                loopVariable = match.group(1).strip()
                dataSrcVariable = match.group(2).strip()
                innerLoopStatement = match.group(3).strip()

                code = '\n'.join(['for %s in %s:' % (loopVariable, self.CONTROL_STRUCTURE_DATASRC_FOR), '\t%s.append(%s)' % (self.CONTROL_STRUCTURE_RETVAL_FOR, innerLoopStatement) ])

                return code, dataSrcVariable
            
            except Exception as e:
                raise('An error occured generating the for loop control structure code')

        return None, None

    

