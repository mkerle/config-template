from tests.templateTests.baseTemplateTest import JSON_TEMPLATE_VALID_PATH, JSON_TEMPLATE_INVALID_PATH

from unittest import TestCase

from configTemplate.template.jsonConfigTemplateSource import JSONConfigTemplateSource
from configTemplate.template.jsonFileConfigTemplateSourceFactory import JSONFileConfigTemplateSourceFactory

class testJSONFileTemplateFactory(TestCase):

    def testCreateJSONTemplateFromFile(self):
        
        template = JSONFileConfigTemplateSourceFactory.createTemplateSource(JSON_TEMPLATE_VALID_PATH)
        self.assertTrue(template is not None, 'JSONFileConfigTemplateFactory.createTemplate() returned None object')       
        self.assertIs(type(template), JSONConfigTemplateSource, 'JSONFileConfigTemplateSourceFactory.createTemplateSource() did not return a JSONConfigTemplate object')        
        self.assertTrue(template.isValidTemplate(), 'isValidTemplate() returned False')

    def testCreateTemplateInvalidFile(self):

        template = JSONFileConfigTemplateSourceFactory.createTemplateSource(JSON_TEMPLATE_INVALID_PATH)
        self.assertIsNone(template, 'JSONFileConfigTemplateFactory.createTemplate() with non-json file returned a template object')

    def testCreateJSONTemplateFileNotExist(self):
        
        self.assertRaises(Exception, JSONFileConfigTemplateSourceFactory.createTemplateSource, 'N0tAValidPathToFile.json', 'Factory method did not raise exception for missing file')