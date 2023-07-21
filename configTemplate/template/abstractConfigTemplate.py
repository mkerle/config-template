from abc import ABC, abstractmethod
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition
from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource

class AbstractConfigTemplate(ABC):

    def __init__(self, 
                 mainTemplateSource : AbstractConfigTemplateSource = None,
                 inheritedTemplatesSources : dict = None,
                 templateDefinition : AbstractTemplateDefinition = AbstractTemplateDefinition()):
        
        self.setTemplateDefinition(templateDefinition)

    def setTemplateDefinition(self, templateDefinition : AbstractTemplateDefinition):
        self._templateDefinition = templateDefinition

    def getTemplateDefinition(self) -> AbstractTemplateDefinition:
        return self._templateDefinition
    
    @abstractmethod
    def render(self, *args, **kwargs) -> any:
        raise NotImplementedError
    
    


    

