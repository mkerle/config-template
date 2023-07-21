from configTemplate.template.abstractConfigTemplateFactory import AbstractConfigTemplateFactory

from configTemplate.template.jsonConfigTemplateSource import JSONConfigTemplateSource
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition
from configTemplate.template.defaultTemplateDefinition import DefaultTemplateDefinition
from configTemplate.template.jsonConfigTemplate import JSONConfigTemplate

class JSONConfigTemplateFactory(AbstractConfigTemplateFactory):

    def __init__(self):
        super().__init__()

    @staticmethod
    def createTemplateFromSource(mainTemplateSource : JSONConfigTemplateSource = None,
                        inheritedTemplatesSources : dict = None,
                        templateDefinition : AbstractTemplateDefinition = DefaultTemplateDefinition()) -> JSONConfigTemplate:
        
        return JSONConfigTemplate(mainTemplateSource, inheritedTemplatesSources, templateDefinition)