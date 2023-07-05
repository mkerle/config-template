from unittest import TestCase

import baseTemplateTest

from configTemplate.template.jsonConfigTemplate import JSONConfigTemplate

class testJSONTemplate(TestCase):

    def testValidJSONTemplate(self):

        result = JSONConfigTemplate.isValidTemplateData(baseTemplateTest.templateObj)
        self.assertTrue(result, 'isValidTemplate() returned False')

    def testCreateSimpleJSONTemplate(self):
        
        template = JSONConfigTemplate(baseTemplateTest.templateObj)

        templateName = template.getTemplateName()
        self.assertTrue(templateName == baseTemplateTest.templateObj['name'], 'getTemplateName() did not return as expected')

        templateVersion = template.getTemplateVersion()
        self.assertTrue(templateVersion == baseTemplateTest.templateObj['version'], 'getTemplateVersion() did not return as expected.')

        templateData = template.getTemplateData()
        self.assertTrue(type(templateData) == dict, 'getTemplateData() is not a dict')
        self.assertTrue(templateData == baseTemplateTest.templateObj['template'], 'getTemplateData() did not return as expected')

    def testValidateJSONTemplate(self):

        self.assertFalse(JSONConfigTemplate.isValidTemplateData(None), 'isValidTemplate() returned true for None type template object')

        self.assertFalse(JSONConfigTemplate.isValidTemplateData([]), 'isValidTemplate() returned true for non dict template object')

        self.assertFalse(JSONConfigTemplate.isValidTemplateData({}), 'isValidTemplate() returned True for empty dict template object')

        templateObj = {'name' : 'Test'}
        self.assertFalse(JSONConfigTemplate.isValidTemplateData(templateObj), 'isValidTemplate() returned true for template object missing version and template')

        templateObj['version'] = 1
        self.assertFalse(JSONConfigTemplate.isValidTemplateData(templateObj), 'isValidTemplate() returned true for template object missing template')

        templateObj['template'] = []
        self.assertFalse(JSONConfigTemplate.isValidTemplateData(templateObj), 'isValidTemplate() returned true for template object with invalid template data type')

        templateObj['template'] = {}
        self.assertTrue(JSONConfigTemplate.isValidTemplateData(templateObj), 'isValidTemplate() returned false for valid template structure')

    def testInheritedTemplates(self):

        templateObj = {
            'name' : 'Test',
            'version' : 1,            
            'template' : {}
        }

        template = JSONConfigTemplate(templateObj)
        self.assertTrue(template.getTemplateInheritedTemplates() == [], 'getTemplateInheritedTemplates() should have returned empty list when not defined in template')

        templateObj['inherit-templates'] = {}

        self.assertRaises(Exception, JSONConfigTemplate.isValidTemplateData(templateObj), 'isValidTemplate() failed to raise exception for invalid type for inherit-templates')

        template = JSONConfigTemplate(templateObj)
        self.assertRaises(Exception, template.getTemplateInheritedTemplates(), 'getTemplateInheritedTemplates() did not raise an exception for invalid inherit-templates type')

        templateObj['inherit-templates'] = []

        self.assertTrue(JSONConfigTemplate.isValidTemplateData(templateObj), 'isValidTemplate() returned False for a valid template structure')


