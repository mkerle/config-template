from configTemplate.template.abstractConfigTemplateSourceFactory import AbstractConfigTemplateSourceFactory
from configTemplate.template.jsonConfigTemplateSource import JSONConfigTemplateSource

import os
import json

class JSONFileConfigTemplateSourceFactory(AbstractConfigTemplateSourceFactory):

    @staticmethod
    def createTemplateSource(inputFilePath : str, *args, **kwargs) -> JSONConfigTemplateSource:

        if (os.path.exists(inputFilePath)):

            try:

                with open(inputFilePath, 'r') as f:

                    templateData = json.load(f)                    

                    if (JSONConfigTemplateSource.isValidTemplateData(templateData)):
                        return JSONConfigTemplateSource(templateData)
                    
            except:
                # Will return None on exception from reading the template
                return None
                    
        else:
            raise Exception('JSON Config Template Source File not found [%s]' % (inputFilePath))
        
        return None

