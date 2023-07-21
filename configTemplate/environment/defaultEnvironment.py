from configTemplate.environment.abstractEnvironment import AbstractEnvironment
from configTemplate.importSource.abstractTemplateImportSource import AbstractTemplateImportSource

class DefaultEnvironment(AbstractEnvironment):

    def __init__(self, importSource : AbstractTemplateImportSource | list = None):

        super().__init__(importSource)


