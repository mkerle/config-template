from abc import ABC, abstractmethod

from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition
from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate

class AbstractConfigTemplateFactory(ABC):

    def __init__(self):
        pass

    @abstractmethod
    @staticmethod
    def createTemplateFromSource(mainTemplateSource : AbstractConfigTemplateSource = None,
                        inheritedTemplatesSources : dict = None,
                        templateDefinition : AbstractTemplateDefinition = AbstractTemplateDefinition()) -> AbstractConfigTemplate:
        
        NotImplementedError()
        
