from configTemplate.importSource.abstractTemplateImportSource import AbstractTemplateImportSource
from configTemplate.importSource.genericTemplateSourceCache import GenericTemplateSourceCache
from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate

from configTemplate.template.abstractConfigTemplateFactory import AbstractConfigTemplateFactory

import os
import pathlib


class DirectoryTemplateImportSource(AbstractTemplateImportSource):

    def __init__(self, directoryPath : str, factoryMethod : AbstractConfigTemplateFactory):

        super.__init__()

        self.directoryPath = directoryPath
        self.factoryMethod = factoryMethod

        self.importSourceCache = GenericTemplateSourceCache()

    def hasTemplate(self, templateName: str, templateVersion : int) -> bool:
        
        return self.importSourceCache.get(templateName, templateVersion) is not None
    
    def _getTemplateFromFilePath(self, templateFilePath : str) -> AbstractConfigTemplate:

        if (os.path.exists(templateFilePath)):

            try:
                return self.factoryMethod.createTemplateFromFile(templateFilePath)
            except:
                Exception('An error occured getting template! Path: [%s]' % (templateFilePath))
            finally:
                return None

        return None
    
    def getTemplate(self, templateName: str, templateVersion: int) -> AbstractConfigTemplate:
        
        templateFilePath = str(self.importSourceCache.get(templateName, templateVersion))

        if (templateFilePath is not None):
            return self._getTemplateFromFilePath(templateFilePath)
        
        return None
    
    def buildCache(self):
        
        importPath = pathlib.Path(self.directoryPath)

        if (importPath.exists()):

            if (importPath.is_dir()):

                for childPath in importPath.iterdir():

                    if (childPath.is_file()):

                        filePath = childPath.as_posix()

                        templateObj = self._getTemplateFromFilePath(filePath)

                        if (templateObj.isValidTemplate()):

                            self.importSourceCache.add(templateObj.getTemplateName(), templateObj.getTemplateVersion(), filePath)

                        else:

                            print('File at [%s] does not contain a valid config template' % (filePath))
                    
                    else:

                        print('Ignoring non-normal file [%s]' % (filePath))

            else:

                Exception('Directory Path [%s] is not a directory!')

        else:

            Exception('Directory Path [%s] does not exist!')