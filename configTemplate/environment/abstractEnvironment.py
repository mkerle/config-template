from abc import ABC, abstractmethod
from configTemplate.importSource.abstractTemplateImportSource import AbstractTemplateImportSource
from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource
from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate
from configTemplate.template.abstractConfigTemplateFactory import AbstractConfigTemplateFactory
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition

import logging
from typing import Union, Tuple, List

class AbstractEnvironment(ABC):

    def __init__(self, importSource : Union[AbstractTemplateImportSource, List[AbstractTemplateImportSource]] = None, 
                    templateFactory : AbstractConfigTemplateFactory = AbstractConfigTemplateFactory,
                    templateDefinition : AbstractTemplateDefinition = AbstractTemplateDefinition()):
        
        self.setTemplateImportSources(importSource)
        self.templateFactory = templateFactory
        self.templateDefinition = templateDefinition
    
    def addTemplateImportSource(self, importSource : AbstractTemplateImportSource):

        if (isinstance(importSource, AbstractTemplateImportSource)):
            self.templateImportSources.append(importSource)
        else:
            raise TypeError('importSource should be an instance of AbstractTemplateImportSource')

    def setTemplateImportSources(self, importSource : Union[AbstractTemplateImportSource, List[AbstractTemplateImportSource]]):

        self.templateImportSources = []

        if (type(importSource) == list):
            for obj in importSource:
                self.addTemplateImportSource(obj)
        else:
            self.addTemplateImportSource(importSource)

    def getTemplateImportSources(self) -> List[AbstractTemplateImportSource]:

        return self.templateImportSources
    
    def _getImportetdTemplateSources(self, templateSource : AbstractConfigTemplateSource, importedTemplateSources : dict) -> dict:

        for importedTemplate in templateSource.getTemplateImports():            

            importedTemplateName = importedTemplate['name']
            
            logging.debug('AbstractEnvironment._getImportetdTemplateSources() -> Looing for imported template: [%s]' % importedTemplateName)

            importedTemplateSource = self._getTemplateSource(importedTemplateName)

            if (importedTemplateSource is None):
                raise Exception('Unable to find imported template [name=%s]' % importedTemplateName)
            
            importedTemplateSources[importedTemplateName] = importedTemplateSource
            importedTemplateSources = self._getImportetdTemplateSources(importedTemplateSource, importedTemplateSources)

        return importedTemplateSources
    
    def _getTemplateSource(self, templateName : str) -> AbstractConfigTemplateSource:

        templateSource = None
        for importSource in self.getTemplateImportSources():            

            importSource.refreshCache()
            templateSource = importSource.getTemplate(templateName)

            if (templateSource is not None):
                return templateSource

        return templateSource

    def getTemplate(self, templateName : str) -> AbstractConfigTemplate:

        logging.debug('AbstractEnvironment.getTemplate() -> Looking for requested template [%s]' % (templateName))

        templateSource = self._getTemplateSource(templateName)

        if (templateSource is not None):
            importedTemplateSources = self._getImportetdTemplateSources(templateSource, {})
            return self.templateFactory.createTemplateFromSource(templateSource, importedTemplateSources, self.templateDefinition)
        
        return None

