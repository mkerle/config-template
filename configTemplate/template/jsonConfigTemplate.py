from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate

class JSONConfigTemplate(AbstractConfigTemplate):

    FIELD_TEMPLATE_NAME = 'name'
    FIELD_TEMPLATE_VERSION = 'version'
    FIELD_TEMPLATE_DATA = 'template'
    FIELD_TEMPLATE_INHERIT = 'inherited-templates'

    def __init__(self, templateData : dict = None):
        super().__init__(templateData)

        if (templateData is not None):
            self.templateObj = templateData
        else:
            self.setTemplateData(templateData)

    def setTemplateData(self, templateData: dict):
        
        if (JSONConfigTemplate.isValidTemplate(templateData)):
            self.templateObj = templateData

        raise Exception('JSON Template is not valid')
    
    def _templateObjIsDict(templateObj : dict) -> bool:

        return type(templateObj == dict)

    def _hasTemplateName(templateObj : dict) -> bool:

        if (JSONConfigTemplate._templateObjIsDict(templateObj)):
            return JSONConfigTemplate.FIELD_TEMPLATE_NAME in templateObj
        
        return False
        
    def _hasTemplateVersion(templateObj : dict) -> bool:

        if (JSONConfigTemplate._templateObjIsDict(templateObj)):
            return JSONConfigTemplate.FIELD_TEMPLATE_VERSION in templateObj
        
        return False
        
    def _hasTemplateData(templateObj : dict) -> bool:

        if (JSONConfigTemplate._templateObjIsDict(templateObj)):
            if (JSONConfigTemplate.FIELD_TEMPLATE_DATA in templateObj):
                return type(templateObj[JSONConfigTemplate.FIELD_TEMPLATE_DATA]) == dict
            
        else:
            raise Exception('Template data [%s] is not of type dict' % (JSONConfigTemplate.FIELD_TEMPLATE_DATA))
            
        return False
    
    def _hasTemplateInheritedTemplates(templateObj : dict) -> bool:

        if (JSONConfigTemplate._templateObjIsDict(templateObj)):
            if (JSONConfigTemplate.FIELD_TEMPLATE_INHERIT in templateObj):
                return type(templateObj[JSONConfigTemplate.FIELD_TEMPLATE_INHERIT]) == list
            
        else:
            raise Exception('Template field [%s] is not of type list' % (JSONConfigTemplate.FIELD_TEMPLATE_INHERIT))
            
        return False

    def _getTemplateName(templateObj : dict) -> str:

        if (JSONConfigTemplate._hasTemplateName(templateObj)):
            return templateObj[JSONConfigTemplate.FIELD_TEMPLATE_NAME]
        
        raise Exception('No template name defined!')
    
    def _getTemplateVersion(templateObj : dict) -> int:

        if (JSONConfigTemplate._hasTemplateVersion(templateObj)):
            return templateObj[JSONConfigTemplate.FIELD_TEMPLATE_VERSION]
        
        raise Exception('No template version defined!')
        
    def _getTemplateData(templateObj : dict) -> dict:

        if (JSONConfigTemplate._hasTemplateData(templateObj)):
            return templateObj[JSONConfigTemplate.FIELD_TEMPLATE_DATA]
        
        raise Exception('No template data defined!')
    
    def _getTemplateInheritedTemplates(templateObj : dict) -> list:

        if (JSONConfigTemplate._hasTemplateInheritedTemplates(templateObj)):
            return templateObj[JSONConfigTemplate.FIELD_TEMPLATE_DATA]
        
        # inherited templates is optional - return empty list
        return []

    def getTemplateName(self) -> str:
        return JSONConfigTemplate._getTemplateName(self.templateObj)
    
    def getTemplateVersion(self) -> int:
        return JSONConfigTemplate._getTemplateVersion(self.templateObj)
    
    def getTemplateData(self) -> dict:
        return JSONConfigTemplate._getTemplateData(self.templateObj)
    
    def getTemplateInheritedTemplates(self) -> list:
        return JSONConfigTemplate._getTemplateInheritedTemplates(self.templateObj)

    def isValidTemplate(templateData: dict) -> bool:
        
        try:
            if (not JSONConfigTemplate._templateObjIsDict(templateData)):
                return False
            elif (not JSONConfigTemplate._hasTemplateName(templateData)):                
                return False
            elif (not JSONConfigTemplate._hasTemplateVersion(templateData)):                
                return False
            elif (not JSONConfigTemplate._hasTemplateData(templateData)):
                return False
            
            if (not JSONConfigTemplate._hasTemplateInheritedTemplates(templateData)):
                # Inherited templates is optional - exception will be
                # thrown if wrong type
                pass
                                        
            return True
        
        except:
            return False
    
        