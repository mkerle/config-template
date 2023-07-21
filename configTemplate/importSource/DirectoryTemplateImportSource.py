from configTemplate.importSource.abstractTemplateImportSource import AbstractTemplateImportSource
from configTemplate.importSource.genericTemplateSourceCache import GenericTemplateSourceCache
from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource

from configTemplate.template.abstractConfigTemplateSourceFactory import AbstractConfigTemplateSourceFactory

import os
import pathlib


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

        return None
    
    def getTemplate(self, templateName: str, *args, **kwargs) -> AbstractConfigTemplateSource:
        
        templateFilePath = str(self.importSourceCache.get(templateName))

        if (templateFilePath is not None):
            return self._getTemplateFromFilePath(templateFilePath)
        
        return None
    
    def buildCache(self):
        
        self.importSourceCache.clearCache()

        importPath = pathlib.Path(self.directoryPath)

        if (importPath.exists()):

            if (importPath.is_dir()):

                for childPath in importPath.iterdir():

                    if (childPath.is_file()):

                        filePath = childPath.as_posix()

                        templateObj = self._getTemplateFromFilePath(filePath)

                        if (templateObj is not None and templateObj.isValidTemplate()):

                            self.importSourceCache.add(templateObj.getTemplateName(), filePath)

                        else:

                            print('File at [%s] does not contain a valid config template' % (filePath))
                    
                    else:

                        print('Ignoring non-normal file [%s]' % (filePath))

            else:

                Exception('Directory Path [%s] is not a directory!')

        else:

            Exception('Directory Path [%s] does not exist!')

    def refreshCache(self):

        # more logic could be added to check mtime of directory etc.
        self.clearCache()
        self.buildCache()