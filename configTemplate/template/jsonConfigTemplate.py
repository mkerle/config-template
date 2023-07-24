from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate
from configTemplate.template.jsonConfigTemplateSource import JSONConfigTemplateSource
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition
from configTemplate.template.defaultTemplateDefinition import DefaultTemplateDefinition

import copy

class JSONConfigTemplate(AbstractConfigTemplate):

    def __init__(self, 
                 mainTemplateSource : JSONConfigTemplateSource = None,
                 inheritedTemplatesSources : dict = None,
                 templateDefinition : AbstractTemplateDefinition = DefaultTemplateDefinition()):
        
        super().__init__(mainTemplateSource, inheritedTemplatesSources, templateDefinition)

        self.mainTemplateSource = mainTemplateSource
        self.inheritedTemplateSources = inheritedTemplatesSources
        self.resolvedTemplates = {}

    def _mergeDict(self, origData : dict, mergeData : dict) -> dict:

        print('Merging data')

        for k in mergeData:
            if (k not in origData):
                origData[k] = mergeData[k]

            elif (type(mergeData[k]) == dict):
                origData[k] = self._mergeDict(origData[k], mergeData[k])

            elif (type(mergeData[k]) == list):
                for listVal in mergeData[k]:
                    if (listVal not in origData[k]):
                        origData[k].append(listVal)

        return origData

    def _handleInsertBlock(self, obj : dict | list, index : str | int, *args, **kwargs):

        if (type(index) == str):

            print('Processing %s' % (index))

            if (index == self.getTemplateDefinition().getImportBlockVariableName()):

                print('Found import variable')

                if (type(obj) == dict):                    
                    if (type(obj[index]) == list):

                        for importSourceTemplateName in obj[index]:

                            if (type(importSourceTemplateName) == str):
                                sourceTemplate = self.inheritedTemplateSources.get(importSourceTemplateName, None)

                                if (sourceTemplate is None):
                                    raise Exception('Unable to find source template for template. [Source Name=%s]' % (importSourceTemplateName))
                                
                                sourceBlock = copy.deepcopy(sourceTemplate.getTemplateData())
                                self._traverseObj(sourceBlock, self._handleInsertBlock, *args, **kwargs)

                                # merge the data
                                obj = self._mergeDict(obj, sourceBlock)

                            else:
                                raise Exception('Expected str for inherited template source name!')
                        
                    else:
                        raise Exception('Import source block type should be a list!')
                    
                else:
                    raise Exception('Import source blocks only supported inside a dictionary at this stage.')
                
        return obj
                                

    def _traverseObjOrig(self, obj, callback, *args, **kwargs) -> any:

        if (type(obj) == dict):
            
            for k in obj:
                
                if (self.getTemplateDefinition().isTemplateKeyword(k)):
                    obj = callback(obj, k, *args, **kwargs)
                
                if (type(obj[k]) == dict or type(obj[k]) == list):
                    obj[k] = self._traverseObj(obj[k], callback)
                else:
                    obj = callback(obj, k, *args, **kwargs)

        elif (type(obj) == list):

            for i in range(0, len(obj)):
                if (type(obj[i]) == dict or type(obj[i]) == list):
                    obj[i] = self._traverseObj(obj[i], callback)
                else:
                    obj = callback(obj, i, *args, **kwargs)

        return obj
    
    def _getxpathStr(self, index : str | int) -> str:

        if (type(index) == str):
            return '["%s"]' % index
        elif (type(index) == int):
            return '[%d]' % index
        
        raise Exception('Invalid type used as index to calculate xpath: [%s]' % (str(index)))
    
    def _traverseObj(self, obj, callback, callbackRetObj : any, xpath : str, *args, **kwargs):

        if (type(obj) == dict):
            
            for k in obj:

                objXpath = xpath + self._getxpathStr(k)
                
                if (type(obj[k]) == dict or type(obj[k]) == list):                    
                    callbackRetObj = self._traverseObj(obj[k], callback, callbackRetObj, objXpath, *args, **kwargs)
                else:                    
                    callbackRetObj = callback(obj, k, callbackRetObj, objXpath, *args, **kwargs)

        elif (type(obj) == list):

            for i in range(0, len(obj)):

                objXpath = xpath + self._getxpathStr(i)

                if (type(obj[i]) == dict or type(obj[i]) == list):                    
                    callbackRetObj = self._traverseObj(obj[i], callback, callbackRetObj, objXpath, *args, **kwargs)
                else:                    
                    callbackRetObj = callback(obj, i, callbackRetObj, objXpath, *args, **kwargs)

        return callbackRetObj

    def _addElementToFlatternedDict(self, obj, index : str | int, callbackRetObj : dict, xpath : str, *args, **kwargs) -> dict:
        
        callbackRetObj[xpath] = obj[index]
        return callbackRetObj

    
    def _mergeAndUpdate(self, mergeData : dict | list, origData : dict | list):
                
        for k in mergeData:
            
            if (k == self.getTemplateDefinition().getImportBlockVariableName()):
                for inheritedTemplateSourceName in mergeData[k]:
                    if (inheritedTemplateSourceName not in self.resolvedTemplates):
                        if inheritedTemplateSourceName not in self.inheritedTemplateSources:
                            raise Exception('Could not find inherited template source to resolve: [%s]' % (inheritedTemplateSourceName))
                        self.resolveTemplateSource(self.inheritedTemplateSources[inheritedTemplateSourceName])
                    
                    origData = self._mergeAndUpdate(self.resolvedTemplates[inheritedTemplateSourceName], origData)

                del origData[k]

            elif (k not in origData):
                origData[k] = mergeData[k]

            elif (type(mergeData[k]) == dict):
                origData[k] = self._mergeAndUpdate(origData[k], mergeData[k])

            elif (type(mergeData[k]) == list):
                for listVal in mergeData[k]:
                    if (listVal not in origData[k]):
                        origData[k].append(listVal)

        return origData
    
    def resolveTemplateSource(self, templateSource : JSONConfigTemplateSource):

        if (templateSource.getTemplateName() not in self.resolvedTemplates):

            print('Resolving template source [%s]...' % (templateSource.getTemplateName()))

            resolvedTemplate = self._mergeAndUpdate(templateSource.getTemplateData(), copy.deepcopy(templateSource.getTemplateData()))

            self.resolvedTemplates[templateSource.getTemplateName()] = resolvedTemplate

        else:

            print('Template source [%s] already resolved' % (templateSource.getTemplateName()))


    def flatternResolvedTemplate(self, resolvedTemplate : dict) -> dict:

        return self._traverseObj(resolvedTemplate, self._addElementToFlatternedDict, {}, '$')
    
    def _isVariable(self, val : str) -> bool:

        return type(val) == str \
                and val.startswith(self.getTemplateDefinition().getVariableStart()) \
                and val.endswith(self.getTemplateDefinition().getVariableEnd())
    
    def _getVariableFromArgs(self, templateVariableName : str, *args, **kwargs) -> any:

        if (templateVariableName in kwargs):
            return kwargs[templateVariableName]
        
        variableParts = templateVariableName.split('.')
        if (len(variableParts) <= 2):
            if (variableParts[0] in kwargs):
                try:
                    return getattr(kwargs[variableParts[0], variableParts[1]])
                    
                except:

                    try:
                        return kwargs[variableParts[0]].__getitem__(variableParts[1])
                    except:
                        raise Exception('Unable to find variable "%s" in supplied arguments' % (templateVariableName))
                    
            else:
                raise Exception('Unable to find variable "%s" in supplied arguments' % (templateVariableName))

        else:
            raise Exception('Variable "%s" is not supported - too many levels' % (templateVariableName))
    
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

                    if (self._isVariable(val)):

                        parsedValue = val[2:-2]

                        obj = self._getVariableFromArgs(parsedValue, *args, **kwargs)

                        if (callable(obj)):
                            obj(xpath, flatternedTemplate, *args, **kwargs)

                        else:
                            flatternedTemplate[xpath] = obj

                        
            variableLevel += 1
                        
        return flatternedTemplate
    
    def _createDictStructureFromXpath(self, xpath : str, unflatternedTemplate : dict, resolvedTemplate : dict) -> dict:
        '''Delete this func'''
        raise NotImplementedError
    
    def _stripXPathName(self, s : str) -> str | int:

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
        self.resolveTemplateSource(self.mainTemplateSource)

        flatternedTemplate = self.flatternResolvedTemplate(self.resolvedTemplates[self.mainTemplateSource.getTemplateName()])

        variableResolvedTemplate = self.resolveTemplateVariables(flatternedTemplate, *args, **kwargs)        

        unflatternedTemplate = self.unflatternTemplate(variableResolvedTemplate, self.resolvedTemplates[self.mainTemplateSource.getTemplateName()])
        
        return unflatternedTemplate

