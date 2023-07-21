from abc import ABC, abstractmethod
from configTemplate.importSource.abstractTemplateImportSource import AbstractTemplateImportSource
from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource
from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate

class AbstractEnvironment(ABC):

    def __init__(self, importSource : AbstractTemplateImportSource | list = None):
        
        self.setTemplateImportSources(importSource)
    
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

        for inheritedTemplate in templateSource.get

    def getTemplate(self, templateName : str) -> AbstractConfigTemplate:

        for importSource in self.getTemplateImportSources():

            importSource.refreshCache()
            template = importSource.getTemplate(templateName)

            if (template is not None):
                return template
            
        return None

