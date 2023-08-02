from configTemplate.importSource.abstractTemplateImportSource import AbstractTemplateImportSource
from configTemplate.importSource.genericTemplateSourceCache import GenericTemplateSourceCache
from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource

from configTemplate.template.abstractConfigTemplateSourceFactory import AbstractConfigTemplateSourceFactory

import os
import pathlib
import logging

class DirectoryTemplateImportSource(AbstractTemplateImportSource):

    def __init__(self, directoryPath : str, factoryMethod : AbstractConfigTemplateSourceFactory):

        super().__init__(directoryPath, factoryMethod)

        self.importSourceCache = GenericTemplateSourceCache()

    def hasTemplate(self, templateName: str, *args, **kwargs) -> bool:
        
        return self.importSourceCache.get(templateName) is not None
    
    def _getTemplateFromFilePath(self, templateFilePath : str) -> AbstractConfigTemplateSource:

        if (os.path.exists(templateFilePath)):

            try:                
                return self.factoryMethod.createTemplateSource(templateFilePath)
            except:
                Exception('An error occured getting template! Path: [%s]' % (templateFilePath))

        logging.warning('DirectoryTemplateImportSource._getTemplateFromFilePath() -> Could not find template at path [%s]' % (templateFilePath))

        return None
    
    def getTemplate(self, templateName: str, *args, **kwargs) -> AbstractConfigTemplateSource:
        
        logging.debug('DirectoryTemplateImportSource.getTemplate() -> Looking for template [%s] in [%s]' % (templateName, self.directoryPath))
        logging.debug('DirectoryTemplateImportSource.getTemplate() -> Cache state: %s' % (str(self.importSourceCache.cache)))

        templateFilePath = str(self.importSourceCache.get(templateName))

        if (templateFilePath is not None):
            logging.debug('DirectoryTemplateImportSource.getTemplate() -> Found template [%s] in cache' % (templateName))
            return self._getTemplateFromFilePath(templateFilePath)
        
        logging.debug('DirectoryTemplateImportSource.getTemplate() -> Could not find template [%s] in cache' % (templateName))
        return None
    
    def buildCache(self):
        
        self.importSourceCache.clearCache()

        importPath = pathlib.Path(self.directoryPath)

        logging.debug('DirectoryTemplateImportSource.buildCache() -> Using directory: %s' % (self.directoryPath))

        if (importPath.exists()):

            if (importPath.is_dir()):

                for childPath in importPath.iterdir():

                    if (childPath.is_file()):

                        filePath = childPath.as_posix()

                        logging.debug('DirectoryTemplateImportSource.buildCache() -> Processing file at [%s]' % (filePath))

                        templateObj = self._getTemplateFromFilePath(filePath)

                        if (templateObj is not None and templateObj.isValidTemplate()):

                            logging.debug('DirectoryTemplateImportSource.buildCache() -> Found valid template [%s] from file [%s] - adding to cache' % (templateObj.getTemplateName(), filePath))

                            self.importSourceCache.add(templateObj.getTemplateName(), filePath)

                        else:

                            logging.debug('DirectoryTemplateImportSource.buildCache() -> File [%s] was not a valid template' % (filePath))
                    
                    else:

                        logging.debug('DirectoryTemplateImportSource.buildCache() -> Ignoring non-normal file [%s]' % (childPath.as_posix()))

            else:

                Exception('Directory Path [%s] is not a directory!')

        else:

            Exception('Directory Path [%s] does not exist!')

    def refreshCache(self):

        # more logic could be added to check mtime of directory etc.
        self.clearCache()
        self.buildCache()