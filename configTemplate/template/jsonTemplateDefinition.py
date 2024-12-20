from typing import Union, Tuple, List
import re

from configTemplate.template.defaultTemplateDefinition import DefaultTemplateDefinition

class JSONTemplateDefinition(DefaultTemplateDefinition):

    CONTROL_STRUCTURE_REGEX_FOR_LIST = r'{%\s+for\s+(.*?)\s+in\s+(.*?)\s+(kwargs(?:\s+)?=(?:\s+)?\[.*\]\s+)?%}'
    CONTROL_STRUCTURE_REGEX_ENDOR_LIST = r'{%\s+endfor\s+%}'

    def __init__(self):
        super().__init__()

    def getTypeOfControlStructure(self, var : Union[str, List]) -> Union[str, None]:        

        if (type(var) == list):
            
            if (len(var) >= 3):
                if (type(var[0]) == str):
                    if re.match(self.CONTROL_STRUCTURE_REGEX_FOR_LIST, var[0]):
                        if (type(var[-1]) == str):
                            if (re.match(self.CONTROL_STRUCTURE_REGEX_ENDOR_LIST, var[-1])):
                                return self.CONTROL_STRUCTURE_TYPE_FOR

        return super().getTypeOfControlStructure(var)

    def getForListControlStructureCode(self, var : List) -> Tuple[str, str, any]:

        if (self.getTypeOfControlStructure(var) == self.CONTROL_STRUCTURE_TYPE_FOR):

            try:

                match = re.match(self.CONTROL_STRUCTURE_REGEX_FOR_LIST, var[0])

                loopVariable = match.group(1).strip()
                dataSrcVariable = match.group(2).strip()

                try:
                    dataSrcKeywordArgStr = match.group(3)
                except IndexError as e:
                    dataSrcKeywordArgStr = None

                if (dataSrcKeywordArgStr is not None):
                    dataSrcKeywordArgDictStr = ''.join(dataSrcKeywordArgStr.split('=')[1:])

                    try:
                        dataSrcKeywordArgs = eval(dataSrcKeywordArgDictStr)

                    except Exception as e:
                        raise Exception('getForListControlStructureCode() -> Error evaluating for loop kwargs! str=%s' % (dataSrcKeywordArgDictStr))
                else:
                    dataSrcKeywordArgs = []


                innerObjects = var[1:-1]

                code = '\n'.join(['for %s in %s:' % (loopVariable, self.CONTROL_STRUCTURE_DATASRC_FOR), '\t%s = %s + loopCallback(loopData=%s, %s=%s, **kwargs)' % (self.CONTROL_STRUCTURE_RETVAL_FOR, self.CONTROL_STRUCTURE_RETVAL_FOR, innerObjects, loopVariable, loopVariable) ])

                callbackKwargs = [ 'loopData', loopVariable ]

                return code, dataSrcVariable, dataSrcKeywordArgs, callbackKwargs

            except Exception as e:
                raise('An error occured generating the for loop control structure code from a list')

        return None, None


            