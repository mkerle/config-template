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
    
    def _traverseObj(self, obj, callback, *args, **kwargs) -> any:

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


    def render(self, *args, **kwargs) -> any:
        '''
        1. Setup initial template
        2. Fill out inherited blocks
        3. Process variables and logic
        '''
        
        #renderedTemplate = copy.deepcopy(self.mainTemplateSource.getTemplateData())

        self.resolvedTemplates = {}
        self.resolveTemplateSource(self.mainTemplateSource)

        #renderedTemplate = self._traverseObj(renderedTemplate, self._handleInsertBlock, *args, **kwargs)

        return self.resolvedTemplates[self.mainTemplateSource.getTemplateName()]

