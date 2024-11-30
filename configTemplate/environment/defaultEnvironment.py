from configTemplate.environment.abstractEnvironment import AbstractEnvironment
from configTemplate.importSource.abstractTemplateImportSource import AbstractTemplateImportSource
from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource
from configTemplate.template.abstractConfigTemplateFactory import AbstractConfigTemplateFactory
from configTemplate.template.abstractTemplateDefinition import AbstractTemplateDefinition

from typing import Union, Tuple, List

class DefaultEnvironment(AbstractEnvironment):

    def __init__(self, importSource : Union[AbstractTemplateImportSource, List[AbstractTemplateImportSource]] = None, 
                    templateFactory : AbstractConfigTemplateFactory = AbstractConfigTemplateFactory,
                    templateDefinition : AbstractTemplateDefinition = AbstractTemplateDefinition()):

        super().__init__(importSource, templateFactory, templateDefinition)


