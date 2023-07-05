from configTemplate.template.abstractConfigTemplateFactory import AbstractConfigTemplateFactory
from configTemplate.template.jsonConfigTemplate import JSONConfigTemplate

import os
import json

class JSONFileConfigTemplateFactory(AbstractConfigTemplateFactory):

    @staticmethod
    def createTemplate(inputFilePath : str, *args, **kwargs) -> JSONConfigTemplate:

        if (os.path.exists(inputFilePath)):

            try:

                with open(inputFilePath, 'r') as f:

                    templateData = json.load(f)                    

                    if (JSONConfigTemplate.isValidTemplateData(templateData)):
                        return JSONConfigTemplate(templateData)
                    
            except:
                # Will return None on exception from reading the template
                return None
                    
        else:
            raise Exception('JSON Config Template File not found [%s]' % (inputFilePath))
        
        return None

