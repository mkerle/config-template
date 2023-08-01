from abc import ABC, abstractmethod
from configTemplate.importSource.abstractTemplateImportSource import AbstractTemplateImportSource
from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource
from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate
from configTemplate.template.abstractConfigTemplateFactory import AbstractConfigTemplateFactory
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition

import logging

class AbstractEnvironment(ABC):

    def __init__(self, importSource : AbstractTemplateImportSource | list = None, 
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

    def setTemplateImportSources(self, importSource : AbstractTemplateImportSource | list):

        self.templateImportSources = []

        if (type(importSource) == list):
            for obj in importSource:
                self.addTemplateImportSource(obj)
        else:
            self.addTemplateImportSource(importSource)

    def getTemplateImportSources(self) -> list:

        return self.templateImportSources
    
    def _getInheritedTemplateSources(self, templateSource : AbstractConfigTemplateSource, inheritedTemplateSources : dict) -> dict:

        for inheritedTemplate in templateSource.getTemplateInheritedTemplates():            

            inheritedTemplateName = inheritedTemplate['name']
            
            logging.debug('AbstractEnvironment._getInheritedTemplateSources() -> Looing for inherited template: [%s]' % (inheritedTemplateName))

            inheritedTemplateSource = self._getTemplateSource(inheritedTemplateName)

            if (inheritedTemplateSource is None):
                raise Exception('Unable to find inherited template [name=%s]' % (inheritedTemplateName))
            
            inheritedTemplateSources[inheritedTemplateName] = inheritedTemplateSource
            inheritedTemplateSources = self._getInheritedTemplateSources(inheritedTemplateSource, inheritedTemplateSources)

        return inheritedTemplateSources
    
    def _getTemplateSource(self, templateName : str) -> AbstractConfigTemplateSource:

        templateSource = None
        for importSource in self.getTemplateImportSources():            

            importSource.refreshCache()
            templateSource = importSource.getTemplate(templateName)

        return templateSource

    def getTemplate(self, templateName : str) -> AbstractConfigTemplate:

        logging.debug('AbstractEnvironment.getTemplate() -> Looking for requested template [%s]' % (templateName))

        templateSource = self._getTemplateSource(templateName)

        if (templateSource is not None):
            inheritedTemplateSources = self._getInheritedTemplateSources(templateSource, {})
            return self.templateFactory.createTemplateFromSource(templateSource, inheritedTemplateSources, self.templateDefinition)
        
        return None

