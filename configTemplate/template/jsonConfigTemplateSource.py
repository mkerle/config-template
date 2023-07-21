from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource
from configTemplate.template.defaultTemplateDefinition import DefaultTemplateDefinition

class JSONConfigTemplateSource(AbstractConfigTemplateSource):

    FIELD_TEMPLATE_NAME = 'name'
    FIELD_TEMPLATE_VERSION = 'version'
    FIELD_TEMPLATE_DATA = 'template'
    FIELD_TEMPLATE_INHERIT = 'inherited-templates'

    def __init__(self, 
                 templateData : dict = None):
        
        super().__init__(templateData)
        
        self.setTemplateData(templateData)

    def setTemplateData(self, templateData: dict):
        
        if (templateData is None):
            self.templateObj = None
        elif (JSONConfigTemplateSource.isValidTemplateData(templateData)):
            self.templateObj = templateData
        else:
            raise Exception('JSON Template is not valid')
    
    def _templateObjIsDict(templateObj : dict) -> bool:

        return type(templateObj == dict)

    def _hasTemplateName(templateObj : dict) -> bool:

        if (JSONConfigTemplateSource._templateObjIsDict(templateObj)):
            return JSONConfigTemplateSource.FIELD_TEMPLATE_NAME in templateObj
        
        return False
        
    def _hasTemplateVersion(templateObj : dict) -> bool:

        if (JSONConfigTemplateSource._templateObjIsDict(templateObj)):
            return JSONConfigTemplateSource.FIELD_TEMPLATE_VERSION in templateObj
        
        return False
        
    def _hasTemplateData(templateObj : dict) -> bool:

        if (JSONConfigTemplateSource._templateObjIsDict(templateObj)):
            if (JSONConfigTemplateSource.FIELD_TEMPLATE_DATA in templateObj):
                return type(templateObj[JSONConfigTemplateSource.FIELD_TEMPLATE_DATA]) == dict
            
        else:
            raise Exception('Template data [%s] is not of type dict' % (JSONConfigTemplateSource.FIELD_TEMPLATE_DATA))
            
        return False
    
    def _hasTemplateInheritedTemplates(templateObj : dict) -> bool:

        if (JSONConfigTemplateSource._templateObjIsDict(templateObj)):
            if (JSONConfigTemplateSource.FIELD_TEMPLATE_INHERIT in templateObj):
                return type(templateObj[JSONConfigTemplateSource.FIELD_TEMPLATE_INHERIT]) == list
            
        else:
            raise Exception('Template field [%s] is not of type list' % (JSONConfigTemplateSource.FIELD_TEMPLATE_INHERIT))
            
        return False

    def _getTemplateName(templateObj : dict) -> str:

        if (JSONConfigTemplateSource._hasTemplateName(templateObj)):
            return templateObj[JSONConfigTemplateSource.FIELD_TEMPLATE_NAME]
        
        raise Exception('No template name defined!')
    
    def _getTemplateVersion(templateObj : dict) -> int:

        if (JSONConfigTemplateSource._hasTemplateVersion(templateObj)):
            return templateObj[JSONConfigTemplateSource.FIELD_TEMPLATE_VERSION]
        
        raise Exception('No template version defined!')
        
    def _getTemplateData(templateObj : dict) -> dict:

        if (JSONConfigTemplateSource._hasTemplateData(templateObj)):
            return templateObj[JSONConfigTemplateSource.FIELD_TEMPLATE_DATA]
        
        raise Exception('No template data defined!')
    
    def _getTemplateInheritedTemplates(templateObj : dict) -> list:

        if (JSONConfigTemplateSource._hasTemplateInheritedTemplates(templateObj)):
            return templateObj[JSONConfigTemplateSource.FIELD_TEMPLATE_DATA]
        
        # inherited templates is optional - return empty list
        return []

    def getTemplateName(self) -> str:
        return JSONConfigTemplateSource._getTemplateName(self.templateObj)
    
    def getTemplateVersion(self) -> int:
        return JSONConfigTemplateSource._getTemplateVersion(self.templateObj)
    
    def getTemplateData(self) -> dict:
        return JSONConfigTemplateSource._getTemplateData(self.templateObj)
    
    def getTemplateInheritedTemplates(self) -> list:
        return JSONConfigTemplateSource._getTemplateInheritedTemplates(self.templateObj)
    
    def isValidTemplate(self) -> bool:
        return JSONConfigTemplateSource.isValidTemplateData(self.templateObj)

    @staticmethod
    def isValidTemplateData(templateData: dict) -> bool:
        
        try:
            if (not JSONConfigTemplateSource._templateObjIsDict(templateData)):
                return False
            elif (not JSONConfigTemplateSource._hasTemplateName(templateData)):                
                return False
            elif (not JSONConfigTemplateSource._hasTemplateVersion(templateData)):                
                return False
            elif (not JSONConfigTemplateSource._hasTemplateData(templateData)):
                return False
            
            if (not JSONConfigTemplateSource._hasTemplateInheritedTemplates(templateData)):
                # Inherited templates is optional - exception will be
                # thrown if wrong type
                pass
                                        
            return True
        
        except:
            return False
        