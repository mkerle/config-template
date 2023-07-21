from unittest import TestCase

from configTemplate.importSource.directoryTemplateImportSource import DirectoryTemplateImportSource
from configTemplate.template.jsonFileConfigTemplateSourceFactory import JSONFileConfigTemplateSourceFactory
from configTemplate.template.abstractConfigTemplateSource import AbstractConfigTemplateSource

from tests.baseTest import EXAMPLE_TEMPLATE_DIR, BASIC_JSON_TEMPLATE_NAME

class testDirectoryTemplateImportSource(TestCase):

    def testDirectoryImportSource(self):

        importSource = DirectoryTemplateImportSource(EXAMPLE_TEMPLATE_DIR, JSONFileConfigTemplateSourceFactory)

        importSource.buildCache()

        template = importSource.getTemplate(BASIC_JSON_TEMPLATE_NAME)

        self.assertIsNotNone(template, 'Returned template is none!')
        self.assertIsInstance(template, AbstractConfigTemplateSource)
        self.assertTrue(template.getTemplateName() == BASIC_JSON_TEMPLATE_NAME, 'Returned template has a different name')


