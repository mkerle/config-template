from configTemplate.importSource.abstractTemplateSourceCache import AbstractTemplateSourceCache
from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate

class GenericTemplateSourceCache(AbstractTemplateSourceCache):

    def __init__(self):

        super.__init__()

    def _getCacheKey(self, templateName : str, templateVersion : int) -> str:

        return templateName + '___' + str(templateVersion)

    def add(self, templateName : str, templateVersion : int, obj : any = None):

        cacheKey = self._getCacheKey(templateName, templateVersion)
        if (cacheKey not in self.cache):
            self.cache[cacheKey] = obj

        else:
            raise Exception('Duplicate cache key found for template')
        
    def get(self, templateName : str, templateVersion : int) -> any:

        cacheKey = self._getCacheKey(templateName, templateVersion)
        if (cacheKey in self.cache):
            return self.cache[cacheKey]
        
        return None

