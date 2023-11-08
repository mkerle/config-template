from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate
from configTemplate.template.jsonConfigTemplateSource import JSONConfigTemplateSource
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition
from configTemplate.template.jsonTemplateDefinition import JSONTemplateDefinition

import copy
import logging
from typing import Union, Tuple

class JSONConfigTemplate(AbstractConfigTemplate):

    def __init__(self, 
                 mainTemplateSource : JSONConfigTemplateSource = None,
                 importedTemplatesSources : dict = None,
                 templateDefinition : AbstractTemplateDefinition = JSONTemplateDefinition()):
        
        super().__init__(mainTemplateSource, importedTemplatesSources, templateDefinition)

        self.mainTemplateSource = mainTemplateSource
        self.importedTemplatesSources = importedTemplatesSources
        self.resolvedTemplates = {}

    def _getxpathStr(self, index : Union[str, int]) -> str:

        if (type(index) == str):
            return '["%s"]' % index
        elif (type(index) == int):
            return '[%d]' % index
        
        raise Exception('Invalid type used as index to calculate xpath: [%s]' % (str(index)))
    
    def _traverseObj(self, obj, callback, callbackRetObj : any, xpath : str, *args, **kwargs):

        if (type(obj) == dict):

            if (len(obj) < 1):
                # handle special cases for empty dicts
                if (type(callbackRetObj) == dict):
                    callbackRetObj[xpath] = {}
            
            for k in obj:

                objXpath = xpath + self._getxpathStr(k)
                
                if (type(obj[k]) == dict or type(obj[k]) == list):                    
                    callbackRetObj = self._traverseObj(obj[k], callback, callbackRetObj, objXpath, *args, **kwargs)
                else:                    
                    callbackRetObj = callback(obj, k, callbackRetObj, objXpath, *args, **kwargs)

        elif (type(obj) == list):

            if (len(obj) < 1):
                # handle special cases for empty lists
                if (type(callbackRetObj) == dict):
                    callbackRetObj[xpath] = []


            for i in range(0, len(obj)):

                objXpath = xpath + self._getxpathStr(i)

                if (type(obj[i]) == dict or type(obj[i]) == list):                    
                    callbackRetObj = self._traverseObj(obj[i], callback, callbackRetObj, objXpath, *args, **kwargs)
                else:                    
                    callbackRetObj = callback(obj, i, callbackRetObj, objXpath, *args, **kwargs)

        return callbackRetObj

    def _addElementToFlatternedDict(self, obj, index : Union[str, int], callbackRetObj : dict, xpath : str, *args, **kwargs) -> dict:
        
        callbackRetObj[xpath] = obj[index]
        return callbackRetObj

    def _loopCallbackMerge(self, *args, **kwargs) -> list:

        if ('loopData' not in kwargs):
            raise Exception('Expected to find "loopData" in kwargs but it was not found.')

        mergeData = kwargs['loopData']

        if (type(mergeData) == list):
            
            localMergeData = { 'mergedata' : mergeData  }

            localMergedData = self._mergeAndUpdateV2(localMergeData, copy.deepcopy(localMergeData), *args, **kwargs)

            flatternedTemplate = self.flatternResolvedTemplate(localMergedData)

            variableResolvedTemplate = self.resolveTemplateVariables(flatternedTemplate, *args, **kwargs)        

            unflatternedTemplate = self.unflatternTemplate(variableResolvedTemplate, localMergedData)

            return unflatternedTemplate['mergedata']

        raise Exception('kwargs["loopData"] was expected to be of type list.  Instead found type=%s' % (str(type(mergeData))))

    
    def _mergeAndUpdateV2(self, mergeData : Union[dict, list], origData : Union[dict, list], *args, **kwargs) -> Union[dict, list]:

        if (type(mergeData) == dict):

            for k in mergeData:

                if (k == self.getTemplateDefinition().getImportBlockVariableName()):
                    for importedTemplateSourceName in mergeData[k]:
                        if (importedTemplateSourceName not in self.resolvedTemplates):
                            if importedTemplateSourceName not in self.importedTemplatesSources:
                                raise Exception('Could not find imported template source to resolve: [%s]' % importedTemplateSourceName)
                            self.resolveTemplateSource(self.importedTemplatesSources[importedTemplateSourceName], *args, **kwargs)
                        
                        origData = self._mergeAndUpdateV2(self.resolvedTemplates[importedTemplateSourceName], origData, *args, **kwargs)

                elif (k not in origData):
                    origData[k] = copy.deepcopy(mergeData[k])

                origData[k] = self._mergeAndUpdateV2(mergeData[k], origData[k], *args, **kwargs)

        elif (type(mergeData) == list):

            for listVal in mergeData:

                skipPostMerge = False

                if (type(listVal) == str and self.getTemplateDefinition().getTypeOfControlStructure(listVal) == self.getTemplateDefinition().CONTROL_STRUCTURE_TYPE_FOR):

                    code, dataSrcVariable = self.getTemplateDefinition().getForControlStructureCode(listVal)

                    if (code is None or dataSrcVariable is None):
                        raise Exception('Failed to generate for loop code from: %s' % (listVal))
                    
                    if (self.getTemplateDefinition().hasTemplateVariable(dataSrcVariable)):
                        localFlatternedTemplate = self.flatternResolvedTemplate(mergeData)
                        dataSrc = self._evaluateVariable(dataSrcVariable[2:-2], '$', localFlatternedTemplate, *args, **kwargs)
                    else:
                        dataSrc = eval(dataSrcVariable)

                    retVals = []
                    globals = {
                        self.getTemplateDefinition().CONTROL_STRUCTURE_DATASRC_FOR : dataSrc, 
                        self.getTemplateDefinition().CONTROL_STRUCTURE_RETVAL_FOR : retVals
                    }
                    
                    exec(code, globals)

                    if (type(retVals) == list):
                        origData += retVals
                    else:
                        raise Exception('Dont know how to handle type %s from for loop control structure' % (str(type(retVals))))
                    
                    if (listVal in origData):
                        origData.remove(listVal)

                elif (type(listVal) == list and self.getTemplateDefinition().getTypeOfControlStructure(listVal) == self.getTemplateDefinition().CONTROL_STRUCTURE_TYPE_FOR):

                    code, dataSrcVariable = self.getTemplateDefinition().getForListControlStructureCode(listVal)

                    if (code is None or dataSrcVariable is None):
                        raise Exception('Failed to generate for loop code from list: %s' % (listVal))

                    if (self.getTemplateDefinition().hasTemplateVariable(dataSrcVariable)):
                        localFlatternedTemplate = self.flatternResolvedTemplate(mergeData)
                        dataSrc = self._evaluateVariable(dataSrcVariable[2:-2], '$', localFlatternedTemplate, *args, **kwargs)
                    else:
                        dataSrc = eval(dataSrcVariable)

                    retVals = []
                    globals = {
                        self.getTemplateDefinition().CONTROL_STRUCTURE_DATASRC_FOR : dataSrc, 
                        self.getTemplateDefinition().CONTROL_STRUCTURE_RETVAL_FOR : retVals,
                        'loopCallback' : self._loopCallbackMerge
                    }
                    
                    exec(code, globals)

                    if (type(globals[self.getTemplateDefinition().CONTROL_STRUCTURE_RETVAL_FOR]) == list):
                        origData += globals[self.getTemplateDefinition().CONTROL_STRUCTURE_RETVAL_FOR]                        
                    else:
                        raise Exception('Dont know how to handle type %s from for loop control structure (list)' % (str(type(retVals))))
                    
                    if (listVal in origData):                        
                        origData.remove(listVal)

                    # processing of for loop from list syntax will
                    # have already taken care of the merge process
                    # for any dynamiclly created child objects.
                    # skip this at the end
                    skipPostMerge = True

                elif (listVal not in origData):

                    origData.append(listVal)

                if (type(listVal) in [dict, list] and not skipPostMerge):
                    mergeDataListValObj = mergeData[mergeData.index(listVal)]
                    origDataListValObj = origData[origData.index(listVal)]

                    origDataListValObj = self._mergeAndUpdateV2(mergeDataListValObj, origDataListValObj, *args, **kwargs)

        return origData

    
    def resolveTemplateSource(self, templateSource : JSONConfigTemplateSource, *args, **kwargs):

        if (templateSource.getTemplateName() not in self.resolvedTemplates):

            logging.info('jsonConfigTemplate.resolveTemplateSource() -> Resolving template source [%s]...' % (templateSource.getTemplateName()))           

            resolvedTemplate = self._mergeAndUpdateV2(templateSource.getTemplateData(), copy.deepcopy(templateSource.getTemplateData()), *args, **kwargs)

            self.resolvedTemplates[templateSource.getTemplateName()] = resolvedTemplate

        else:

            logging.info('jsonConfigTemplate.resolveTemplateSource() -> Template source [%s] already resolved' % (templateSource.getTemplateName()))


    def flatternResolvedTemplate(self, resolvedTemplate : dict) -> dict:

        return self._traverseObj(resolvedTemplate, self._addElementToFlatternedDict, {}, '$')
    

    def _getVariableFromArgs(self, templateVariableName : str, *args, **kwargs) -> any:

        if (templateVariableName in kwargs):
            return kwargs[templateVariableName]
        
        variableParts = templateVariableName.split('.')
        if (len(variableParts) <= 2):
            if (variableParts[0] in kwargs):
                try:
                    return getattr(kwargs[variableParts[0]], variableParts[1])
                    
                except:

                    try:
                        return kwargs[variableParts[0]].__getitem__(variableParts[1])
                    except:
                        raise Exception('Unable to find variable "%s" in supplied arguments' % (templateVariableName))
                    
            else:
                raise Exception('Unable to find variable "%s" in kwargs' % (templateVariableName))

        else:
            raise Exception('Variable "%s" is not supported - too many levels' % (templateVariableName))
        
    def _evaluateVariable(self, templateVariableName : str, xpath : str, flatternedTemplate : dict, *args, **kwargs) -> any:

        obj = self._getVariableFromArgs(templateVariableName, *args, **kwargs)

        if (callable(obj)):                            
            return obj(xpath, flatternedTemplate, *args, **kwargs)
        else:
            return obj

    def resolveTemplateVariables(self, flatternedTemplate : dict, *args, **kwargs) -> dict:

        variableLevel = 1
        moreVariableLevels = True
        while (moreVariableLevels):

            moreVariableLevels = False

            for xpath in flatternedTemplate:

                numVariableLevels = len(xpath.split('[]'))
                if (numVariableLevels > variableLevel):
                    moreVariableLevels = True
                
                elif (numVariableLevels == variableLevel):

                    val = flatternedTemplate[xpath]

                    if (self.getTemplateDefinition().hasTemplateControlStructure(val)):

                        if (self.getTemplateDefinition().getTypeOfControlStructure(val) == self.getTemplateDefinition().CONTROL_STRUCTURE_TYPE_IF):
                        
                            condition = self.getTemplateDefinition().getIfControlStructureCondition(val)                        

                            evaluatedCondition = self._evaluateVariable(condition, xpath, flatternedTemplate, *args, **kwargs)

                            if (type(evaluatedCondition) == bool):
                                if (evaluatedCondition):
                                    retVal = self.getTemplateDefinition().getIfControlStructureReturnTrue(val)                            
                                else:
                                    retVal = self.getTemplateDefinition().getIfControlStructureReturnFalse(val)                            

                                if (self.getTemplateDefinition().hasTemplateVariable(retVal)):
                                    flatternedTemplate[xpath] = self._evaluateVariable(retVal[2:-2], xpath, flatternedTemplate, *args, **kwargs)
                                else:
                                    flatternedTemplate[xpath] = retVal
                            
                        else:
                            raise Exception('Evaluated logic condition did not return a boolean type: %s' % (condition))

                    elif (self.getTemplateDefinition().hasTemplateVariable(val)):

                        parsedValue = val[2:-2]
                        flatternedTemplate[xpath] = self._evaluateVariable(parsedValue, xpath, flatternedTemplate, *args, **kwargs)


                        
            variableLevel += 1
                        
        return flatternedTemplate
    
    def _stripXPathName(self, s : str) -> Union[str, int]:

        if ('"' in s):
            return s.replace('[', '').replace(']', '').replace('"', '')
        else:
            return int(s.replace('[', '').replace(']', ''))
        
    def _excludePathFromTemplate(self, s : str) -> bool:
        
        if (type(s) == str):
            if (self.getTemplateDefinition().isTemplateKeyword(s)):
                return True
            
        return False
            
    
    def unflatternTemplate(self, flatternedTemplate : dict, resolvedTemplate : dict) -> dict:

        unflatternedTemplate = {}
        for xpath in flatternedTemplate:
            pathParts = xpath[1:].split('[')
            index = 1
            templatePointer = unflatternedTemplate
            resolvedTemplatePointer = resolvedTemplate
            includeInOutput = True
            while (index < len(pathParts)-1):                
                strippedPath = self._stripXPathName(pathParts[index])
                if (self._excludePathFromTemplate(strippedPath)):                    
                    # xpath includes a template only section
                    includeInOutput = False
                    # set the next index so that the loop completes
                    index = len(pathParts)
                elif (type(templatePointer) == dict):
                    if (strippedPath not in templatePointer):
                        if (type(resolvedTemplatePointer[strippedPath]) == dict):
                            templatePointer[strippedPath] = {}
                        elif (type(resolvedTemplatePointer[strippedPath]) == list):
                            templatePointer[strippedPath] = []

                elif (type(templatePointer) == list):
                    if (len(templatePointer) <= strippedPath):
                        if (type(resolvedTemplatePointer[strippedPath]) == dict):
                            templatePointer.append({})
                        elif (type(resolvedTemplatePointer[strippedPath]) == list):
                            templatePointer.append([])
                        
                else:
                    raise Exception('Unknown type of object in template: %s' % (str(type(templatePointer))))                    

                if (includeInOutput):
                    templatePointer = templatePointer[strippedPath]
                    resolvedTemplatePointer = resolvedTemplatePointer[strippedPath]

                index += 1
            
            if (includeInOutput):
                
                if (type(templatePointer) == dict):
                     strippedPath = self._stripXPathName(pathParts[-1])
                     if (not self._excludePathFromTemplate(strippedPath)):
                        templatePointer[strippedPath] = flatternedTemplate[xpath]
                elif (type(templatePointer) == list):
                    templatePointer.append(flatternedTemplate[xpath])

        return unflatternedTemplate            

        

    def render(self, *args, **kwargs) -> any:

        self.resolvedTemplates = {}
        self.resolveTemplateSource(self.mainTemplateSource, *args, **kwargs)

        flatternedTemplate = self.flatternResolvedTemplate(self.resolvedTemplates[self.mainTemplateSource.getTemplateName()])

        variableResolvedTemplate = self.resolveTemplateVariables(flatternedTemplate, *args, **kwargs)        

        unflatternedTemplate = self.unflatternTemplate(variableResolvedTemplate, self.resolvedTemplates[self.mainTemplateSource.getTemplateName()])
        
        return unflatternedTemplate

