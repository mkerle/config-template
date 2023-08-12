from unittest import TestCase

import baseTemplateTest

from configTemplate.template.jsonConfigTemplateSource import JSONConfigTemplateSource

class testJSONTemplateSource(TestCase):

    def testValidJSONTemplateSource(self):

        result = JSONConfigTemplateSource.isValidTemplateData(baseTemplateTest.templateObj)
        self.assertTrue(result, 'isValidTemplate() returned False')

    def testCreateSimpleJSONTemplateSource(self):
        
        template = JSONConfigTemplateSource(baseTemplateTest.templateObj)

        templateName = template.getTemplateName()
        self.assertTrue(templateName == baseTemplateTest.templateObj['name'], 'getTemplateName() did not return as expected')

        templateVersion = template.getTemplateVersion()
        self.assertTrue(templateVersion == baseTemplateTest.templateObj['version'], 'getTemplateVersion() did not return as expected.')

        templateData = template.getTemplateData()
        self.assertTrue(type(templateData) == dict, 'getTemplateData() is not a dict')
        self.assertTrue(templateData == baseTemplateTest.templateObj['template'], 'getTemplateData() did not return as expected')

    def testValidateJSONTemplateSource(self):

        self.assertFalse(JSONConfigTemplateSource.isValidTemplateData(None), 'isValidTemplate() returned true for None type template object')

        self.assertFalse(JSONConfigTemplateSource.isValidTemplateData([]), 'isValidTemplate() returned true for non dict template object')

        self.assertFalse(JSONConfigTemplateSource.isValidTemplateData({}), 'isValidTemplate() returned True for empty dict template object')

        templateObj = {'name' : 'Test'}
        self.assertFalse(JSONConfigTemplateSource.isValidTemplateData(templateObj), 'isValidTemplate() returned true for template object missing version and template')

        templateObj['version'] = 1
        self.assertFalse(JSONConfigTemplateSource.isValidTemplateData(templateObj), 'isValidTemplate() returned true for template object missing template')

        templateObj['template'] = []
        self.assertFalse(JSONConfigTemplateSource.isValidTemplateData(templateObj), 'isValidTemplate() returned true for template object with invalid template data type')

        templateObj['template'] = {}
        self.assertTrue(JSONConfigTemplateSource.isValidTemplateData(templateObj), 'isValidTemplate() returned false for valid template structure')

    def testInheritedTemplateSources(self):

        templateObj = {
            'name' : 'Test',
            'version' : 1,            
            'template' : {}
        }

        template = JSONConfigTemplateSource(templateObj)
        self.assertTrue(template.getTemplateImports() == [], 'getTemplateInheritedTemplates() should have returned empty list when not defined in template')

        templateObj['inherit-templates'] = {}

        self.assertRaises(Exception, JSONConfigTemplateSource.isValidTemplateData(templateObj), 'isValidTemplate() failed to raise exception for invalid type for inherit-templates')

        template = JSONConfigTemplateSource(templateObj)
        self.assertRaises(Exception, template.getTemplateImports(), 'getTemplateInheritedTemplates() did not raise an exception for invalid inherit-templates type')

        templateObj['inherit-templates'] = []

        self.assertTrue(JSONConfigTemplateSource.isValidTemplateData(templateObj), 'isValidTemplate() returned False for a valid template structure')


