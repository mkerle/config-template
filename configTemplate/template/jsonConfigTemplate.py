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

    def _mergeDict(self, origData : dict, mergeData : dict) -> dict:

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

            if (index == self.getTemplateDefinition().getImportBlockVariableName()):

                if (type(obj) == dict):
                    if (type(obj[index]) == str):
                        sourceTemplate = self.inheritedTemplateSources.get(obj[index], None)

                        if (sourceTemplate is None):
                            raise Exception('Unable to find source template for template. [Source Name=%s]' % (sourceTemplate))
                        
                        sourceBlock = copy.deepcopy(sourceTemplate.getTemplateData())
                        self._traverseObj(sourceBlock, self._handleInsertBlock, *args, **kwargs)

                        # merge the data
                        obj = self._mergeDict(obj, sourceBlock)

                    else:
                        raise Exception('Expected str for inherited template source name!')
                    
                else:
                    raise Exception('Import source blocks only supported inside a dictionary at this stage.')
                
        return obj
                                

    def _traverseObj(self, obj, callback, *args, **kwargs) -> any:

        if (type(obj) == dict):

            for k in obj:
                if (type(obj[k]) == dict or type(obj[k]) == list):
                    obj = self._traverseObj(obj[k], callback)
                else:
                    obj = callback(obj, k, *args, **kwargs)
        elif (type(obj) == list):

            for i in range(0, len(obj)):
                if (type(obj[i]) == dict or type(obj[i]) == list):
                    obj = self._traverseObj(obj[i], callback)
                else:
                    obj = callback(obj, i, *args, **kwargs)

    def render(self, *args, **kwargs) -> any:
        
        renderedTemplate = copy.deepcopy(self.mainTemplateSource.getTemplateData())

        renderedTemplate = self._traverseObj(renderedTemplate, self._handleInsertBlock, *args, **kwargs)

        return renderedTemplate

