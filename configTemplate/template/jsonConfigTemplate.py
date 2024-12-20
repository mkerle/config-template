from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate
from configTemplate.template.jsonConfigTemplateSource import JSONConfigTemplateSource
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition
from configTemplate.template.jsonTemplateDefinition import JSONTemplateDefinition

import copy
import logging
from typing import Union, Tuple, List

class JSONConfigTemplate(AbstractConfigTemplate):

    def __init__(self, 
                 mainTemplateSource : JSONConfigTemplateSource = None,
                 importedTemplatesSources : dict = None,
                 templateDefinition : JSONTemplateDefinition = JSONTemplateDefinition()):
        
        super().__init__(mainTemplateSource, importedTemplatesSources, templateDefinition)

        self.mainTemplateSource = mainTemplateSource
        self.importedTemplatesSources = importedTemplatesSources
        self.resolvedTemplates = {}
        self.variableAssignments = {}

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

    def _loopCallbackMerge(self, *args, **kwargs) -> List:

        if ('loopData' not in kwargs):
            raise Exception('Expected to find "loopData" in kwargs but it was not found.')

        mergeData = kwargs['loopData']

        if (type(mergeData) == list):
            
            localMergeData = { 'mergedata' : mergeData  }

            localMergedData = self._resolveControlStructures(localMergeData, copy.deepcopy(localMergeData), *args, **kwargs)

            flatternedTemplate = self.flatternResolvedTemplate(localMergedData)

            variableResolvedTemplate = self.resolveTemplateVariables(flatternedTemplate, *args, **kwargs)        

            unflatternedTemplate = self.unflatternTemplate(variableResolvedTemplate, localMergedData)

            return unflatternedTemplate['mergedata']

        raise Exception('kwargs["loopData"] was expected to be of type list.  Instead found type=%s' % (str(type(mergeData))))

    def _resolveImports(self, mergeData : Union[dict, List], origData : Union[dict, List]) -> Union[dict, List]:
        '''
        This method will return origData with all import statements replaced 
        with the imported template content.
        mergeData in most cases will be the same as origData when the method 
        is initially called and origData wil be modified as import statements
        are found and processed.
        '''        

        if (type(mergeData) == dict):

            for k in mergeData:

                if (k == self.getTemplateDefinition().getImportBlockVariableName()):                    

                    for importedTemplateSourceName in mergeData[k]:
                        if (importedTemplateSourceName not in self.resolvedTemplates):
                            if importedTemplateSourceName not in self.importedTemplatesSources:
                                raise Exception('Could not find imported template source to resolve: [%s]' % importedTemplateSourceName)

                            self.resolvedTemplates[importedTemplateSourceName] = self._resolveImports(self.importedTemplatesSources[importedTemplateSourceName].getTemplateData(), copy.deepcopy(self.importedTemplatesSources[importedTemplateSourceName].getTemplateData()))
                                                
                        origData = self._resolveImports(self.resolvedTemplates[importedTemplateSourceName], origData)

                    del origData[k]

                elif (k not in origData):                    

                    if (type(mergeData[k]) in [dict, list]):

                        origData[k] = self._resolveImports(mergeData[k], copy.deepcopy(mergeData[k]))

                    else:

                        origData[k] = mergeData[k]

                else:

                    if (type(mergeData[k]) in [dict, list]):

                        origData[k] = self._resolveImports(mergeData[k], copy.deepcopy(origData[k]))


        elif (type(mergeData) == list):

            for listval in mergeData:

                if (type(listval) in [list, dict]):

                    mergeListObject = mergeData[mergeData.index(listval)]

                    try:
                        origListObject = origData[origData.index(listval)]
                        origData[origData.index(listval)] = self._resolveImports(mergeListObject, copy.deepcopy(origListObject))
                        
                    except Exception as e:
                        '''
                        This condition can be triggered when in a 
                        "$_merge_list_with_parent" operation with multiple
                        import blocks
                        see test case testMergeWithParentComplex2
                        '''
                        origListObject = mergeListObject                        
                        origData.append(self._resolveImports(mergeListObject, copy.deepcopy(mergeListObject)))

                elif (type(listval) == str and self.getTemplateDefinition().getTypeOfControlStructure(listval) == self.getTemplateDefinition().CONTROL_STRUCTURE_TYPE_IMPORT):
                    
                    importList = self.getTemplateDefinition().getImportControlStructureImportList(listval)
                    
                    struct = self._resolveImports({'$_import_blocks' : importList}, {'$_import_blocks' : importList})
                    origData[origData.index(listval)] = struct                    
                    #origData.append(struct)

                elif (listval not in origData):

                    origData.append(listval)

        return origData
    
    def _parseForLoopKeywordArguments(self, keywordArgs : List[dict]) -> List:
        '''
        The keywordArgs `List` (kwargs) specified in the for loop control structure
        need some parsing on the xpath to ensure that it is formatted correctly.
        This parsing and formating is required to simplify the syntax used in 
        the template to avoid escaping of quotes etc.

        Assumptions are made that all digit indexes will be treated as `int`
        with all other indexes treated as `str`.

        Returns the parsed keywordArgs list.
        '''

        for kwArg in keywordArgs:

            if (type(kwArg) is not dict):
                raise Exception('_parseForLoopKeywordArguments() -> Found a keyword argument that is not of type dict: %s' % (kwArg))
            
            if ('template' not in kwArg):
                raise Exception('_parseForLoopKeywordArguments() -> Keyword argument does not specify the "template": %s' % (kwArg))
            
            if ('variableXpath' not in kwArg):
                raise Exception('_parseForLoopKeywordArguments() -> Keyword argument does not specify the "variableXpath": %s' % (kwArg))
            
            # format the variableXpath to be compatible with this library
            xPathList = []
            for part in kwArg['variableXpath'].split('['):
                if (part == '$'):
                    xPathList.append(part)
                else:
                    
                    # remove the "]"
                    part = part.strip()[:-1]

                    if (part.isdigit()):
                        xPathList.append(int(part))
                    else:
                        xPathList.append(part)

            if (len(xPathList) > 2):
                xPathList.insert(-1, self.getTemplateDefinition().getSetAssignmentVariableName())
            elif (len(xPathList) == 2):
                xPathList.insert(1, self.getTemplateDefinition().getSetAssignmentVariableName())
            else:
                # this is potentially an invalid path
                xPathList.insert(0, self.getTemplateDefinition().getSetAssignmentVariableName())

            kwArg['xPathList'] = xPathList

        return keywordArgs
    
    def _resolveControlStructures(self, mergeData : Union[dict, List], origData : Union[dict, List], *args, **kwargs) -> Union[dict, List]:
        '''
        This method will return origData with all control structure statements 
        executed and replaced with template data content.
        mergeData in most cases will be the same as origData when the method 
        is initially called and origData wil be modified as the control stucture
        statements are found and processed.        
        '''

        if (type(mergeData) == dict):

            for k in mergeData:

                if (k not in origData):
                    origData[k] = copy.deepcopy(mergeData[k])

                origData[k] = self._resolveControlStructures(mergeData[k], origData[k], *args, **kwargs)

        elif (type(mergeData) == list):
            
            for listVal in mergeData:                

                skipPostMerge = False

                if (type(listVal) == str and self.getTemplateDefinition().getTypeOfControlStructure(listVal) == self.getTemplateDefinition().CONTROL_STRUCTURE_TYPE_FOR):

                    code, dataSrcVariable = self.getTemplateDefinition().getForControlStructureCode(listVal)

                    if (code is None or dataSrcVariable is None):
                        raise Exception('Failed to generate for loop code from: %s' % (listVal))
                    
                    if (self.getTemplateDefinition().hasTemplateVariable(dataSrcVariable)):
                        localFlatternedTemplate = self.flatternResolvedTemplate(mergeData)
                        dataSrcVariable, modifiers, varStr = self.getTemplateDefinition().getTemplateVariableParts(dataSrcVariable)
                        dataSrc = self._evaluateVariable(dataSrcVariable, modifiers, '$', localFlatternedTemplate, *args, **kwargs)
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

                    code, dataSrcVariable, dataSrcKeywordArgs, callbackKwargs = self.getTemplateDefinition().getForListControlStructureCode(listVal)                    

                    if (code is None or dataSrcVariable is None):
                        raise Exception('Failed to generate for loop code from list: %s' % (listVal))

                    if (self.getTemplateDefinition().hasTemplateVariable(dataSrcVariable)):

                        dataSrcKwargs = {}
                        if (dataSrcKeywordArgs is not None):
                            dataSrcKeywordArgs = self._parseForLoopKeywordArguments(dataSrcKeywordArgs)

                            for kwArg in dataSrcKeywordArgs:
                                templateName = kwArg['template']
                                variableXpath = kwArg['variableXpath']

                                # check cache
                                cacheKey = templateName + '->' + variableXpath
                                if (cacheKey not in self.variableAssignments):

                                    if (templateName not in self.resolvedTemplates):
                                        self.resolveTemplateSource(self.importedTemplatesSources[templateName])

                                    templateData = self.resolvedTemplates[templateName]
                                    self.resolvedTemplates[templateName] = self._resolveControlStructures(templateData, copy.deepcopy(templateData), *args, **kwargs)

                                    flatternedTemplate = self.flatternResolvedTemplate(self.resolvedTemplates[templateName])

                                    variableResolvedTemplate = self.resolveTemplateVariables(flatternedTemplate, *args, **kwargs)

                                    unflatternedTemplate = self.unflatternTemplate(variableResolvedTemplate, self.resolvedTemplates[templateName], excludeSetAssignmentKeyword=False)

                                    templatePointer = None
                                    for xPathPart in kwArg['xPathList']:

                                        if (xPathPart == '$'):
                                            # init the pointer to root of template
                                            templatePointer = unflatternedTemplate

                                        elif (xPathPart not in templatePointer):
                                            raise Exception('_resolveControlStructures() -> Invalid xpath specified in foor loop kwargs: %s (index=%s, real xpath list: %s) in -> %s' % (variableXpath, xPathPart, kwArg['xPathList'], templatePointer))

                                        else:
                                            templatePointer = templatePointer[xPathPart]

                                    self.variableAssignments[cacheKey] = { 'name' : xPathPart, 'value' : templatePointer['value'] }

                                dataSrcKwargs[self.variableAssignments[cacheKey]['name']] = self.variableAssignments[cacheKey]['value']

                        localFlatternedTemplate = self.flatternResolvedTemplate(mergeData)
                        dataSrcVariable, modifiers, varStr = self.getTemplateDefinition().getTemplateVariableParts(dataSrcVariable)
                        dataSrc = self._evaluateVariable(dataSrcVariable, modifiers, '$', localFlatternedTemplate, *args, **kwargs, **dataSrcKwargs)
                    else:
                        dataSrc = eval(dataSrcVariable)


                    loopKwargs = {}
                    for kwarg in kwargs:
                        if (kwarg not in callbackKwargs):
                            loopKwargs[kwarg] = kwargs[kwarg]

                    retVals = []
                    globals = {
                        self.getTemplateDefinition().CONTROL_STRUCTURE_DATASRC_FOR : dataSrc, 
                        self.getTemplateDefinition().CONTROL_STRUCTURE_RETVAL_FOR : retVals,
                        'loopCallback' : self._loopCallbackMerge,
                        'kwargs' : loopKwargs
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

                elif (type(listVal) == dict and self.getTemplateDefinition().getMergeListWithParentVariableName() in listVal):                    

                    listToMerge = listVal[self.getTemplateDefinition().getMergeListWithParentVariableName()]

                    if (not type(listToMerge) == list):
                        raise Exception('"%s" should be a list! Instead found %s' % (self.getTemplateDefinition().getMergeListWithParentVariableName(), type(listToMerge)))
                    
                    for listMergeObj in listToMerge:

                        if (type(listMergeObj) == list and self.getTemplateDefinition().getTypeOfControlStructure(listMergeObj) == self.getTemplateDefinition().CONTROL_STRUCTURE_TYPE_FOR):
                            # special case for embedded for loop list
                            # note the addition of [] around listMergeObj for origData but not in mergeData
                            listMergeObj = self._resolveControlStructures([listMergeObj], type(listMergeObj)(), *args, **kwargs)                            
                            origData += listMergeObj

                        elif (type(listMergeObj) in [list, dict]):                             
                            origData.append(self._resolveControlStructures(listMergeObj, type(listMergeObj)(), *args, **kwargs))
                        else:
                            origData.append(listMergeObj)

                    if (listVal in origData):
                        origData.remove(listVal)

                    skipPostMerge = True

                elif (listVal not in origData):

                    origData.append(listVal)

                if (type(listVal) in [dict, list] and not skipPostMerge):
                    mergeDataListValObj = mergeData[mergeData.index(listVal)]
                    origDataListValObj = origData[origData.index(listVal)]

                    origDataListValObj = self._resolveControlStructures(mergeDataListValObj, origDataListValObj, *args, **kwargs)
        
        return origData

    
    def resolveTemplateSource(self, templateSource : JSONConfigTemplateSource, *args, **kwargs):

        if (templateSource.getTemplateName() not in self.resolvedTemplates):

            logging.info('jsonConfigTemplate.resolveTemplateSource() -> Resolving template source [%s]...' % (templateSource.getTemplateName()))           

            resolvedTemplate = self._resolveImports(templateSource.getTemplateData(), copy.deepcopy(templateSource.getTemplateData()))

            self.resolvedTemplates[templateSource.getTemplateName()] = resolvedTemplate

        else:

            logging.info('jsonConfigTemplate.resolveTemplateSource() -> Template source [%s] already resolved' % (templateSource.getTemplateName()))

    def resolveTemplateControlStructures(self, *args, **kwargs):

        mainTemplateName = self.mainTemplateSource.getTemplateName()
        mainTemplateData = self.resolvedTemplates[mainTemplateName]

        if (mainTemplateData is not None):

            logging.info('jsonConfigTemplate.resolveTemplateControlStructures() -> Resolving template control structures [%s]...' % (mainTemplateName))

            self.resolvedTemplates[self.mainTemplateSource.getTemplateName()] = self._resolveControlStructures(mainTemplateData, copy.deepcopy(mainTemplateData), *args, **kwargs)


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
        
    def _evaluateVariable(self, templateVariableName : str, modifiers : List[str], xpath : str, flatternedTemplate : dict, *args, **kwargs) -> any:

        obj = self._getVariableFromArgs(templateVariableName, *args, **kwargs)

        parsedModifiers = ''
        for modifier in modifiers:
            if modifier in ['lower', 'upper']:
                parsedModifiers += '.%s()' % (modifier)
            else:
                raise Exception('_evaluateVariable() -> Error! Invalid modifier given: %s.  variable name: %s' % (modifier, templateVariableName))

        if (callable(obj)):
            return eval('obj(xpath, flatternedTemplate, *args, **kwargs)%s' % (parsedModifiers))
        else:
            if (type(obj) is str):
                # if there are any modifiers on a str then we need to eval
                # before returning
                if (len(parsedModifiers) > 0):
                    return eval('"%s"' % (obj) + parsedModifiers)

                return obj + parsedModifiers
            
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

                            evaluatedCondition = self._evaluateVariable(condition, [], xpath, flatternedTemplate, *args, **kwargs)

                            if (type(evaluatedCondition) == bool):
                                if (evaluatedCondition):
                                    retVal = self.getTemplateDefinition().getIfControlStructureReturnTrue(val)                            
                                else:
                                    retVal = self.getTemplateDefinition().getIfControlStructureReturnFalse(val)                            

                                if (self.getTemplateDefinition().hasTemplateVariable(retVal)):
                                    retValVariable, modifiers, varStr = self.getTemplateDefinition().getTemplateVariableParts(retVal)
                                    evalValue = self._evaluateVariable(retValVariable, modifiers, xpath, flatternedTemplate, *args, **kwargs)
                                    if (type(evalValue) == str):
                                        flatternedTemplate[xpath] = val.replace(varStr, evalValue)
                                    else:
                                        flatternedTemplate[xpath] = evalValue
                                else:
                                    flatternedTemplate[xpath] = retVal
                            
                            else:
                                raise Exception('Evaluated logic condition did not return a boolean type: %s' % (condition))

                    elif (self.getTemplateDefinition().hasTemplateVariable(val)):
                        
                        parsedValue, modifiers, varStr = self.getTemplateDefinition().getTemplateVariableParts(val)
                        evalValue = self._evaluateVariable(parsedValue, modifiers, xpath, flatternedTemplate, *args, **kwargs)
                        if (type(evalValue) == str):
                            flatternedTemplate[xpath] = val.replace(varStr, evalValue)
                        else:
                            flatternedTemplate[xpath] = evalValue

                        
            variableLevel += 1
                        
        return flatternedTemplate
    
    def _stripXPathName(self, s : str) -> Union[str, int]:

        if ('"' in s):
            return s.replace('[', '').replace(']', '').replace('"', '')
        else:
            return int(s.replace('[', '').replace(']', ''))
        
    def _excludePathFromTemplate(self, s : str, **kwargs) -> bool:
        
        if (type(s) == str):

            excludeSetAssignmentKeyword = True
            if (kwargs is not None):
                excludeSetAssignmentKeyword = kwargs.get('excludeSetAssignmentKeyword', True)

            if (self.getTemplateDefinition().getSetAssignmentVariableName() == s and not excludeSetAssignmentKeyword):
                return False
            elif (self.getTemplateDefinition().isTemplateKeyword(s)):
                return True
            
        return False
            
    
    def unflatternTemplate(self, flatternedTemplate : dict, resolvedTemplate : dict, **kwargs) -> dict:

        unflatternedTemplate = {}
        for xpath in flatternedTemplate:
            pathParts = xpath[1:].split('[')
            index = 1
            templatePointer = unflatternedTemplate
            resolvedTemplatePointer = resolvedTemplate
            includeInOutput = True
            while (index < len(pathParts)-1):                
                strippedPath = self._stripXPathName(pathParts[index])
                if (self._excludePathFromTemplate(strippedPath, **kwargs)):                    
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
        self.resolveTemplateControlStructures(self.mainTemplateSource, *args, **kwargs)

        flatternedTemplate = self.flatternResolvedTemplate(self.resolvedTemplates[self.mainTemplateSource.getTemplateName()])

        variableResolvedTemplate = self.resolveTemplateVariables(flatternedTemplate, *args, **kwargs)        

        unflatternedTemplate = self.unflatternTemplate(variableResolvedTemplate, self.resolvedTemplates[self.mainTemplateSource.getTemplateName()])
        
        return unflatternedTemplate

