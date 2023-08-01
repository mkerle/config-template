from unittest import TestCase

from tests.baseTest import EXAMPLE_TEMPLATE_DIR, \
                            BASIC_JSON_TEMPLATE_NAME, \
                            COMPLEX_MAIN_JSON_TEMPLATE_NAME, \
                            MULTIPLE_INHERITANCE_JSON_TEMPLATE_NAME, \
                            EXAMPLE_COMMON_TEMPLATE_DIR

import os
import logging

from tests.templateTests.complexJSONTestClass import DeviceSettings

from configTemplate.environment.defaultEnvironment import DefaultEnvironment
from configTemplate.importSource.directoryTemplateImportSource import DirectoryTemplateImportSource
from configTemplate.template.jsonFileConfigTemplateSourceFactory import JSONFileConfigTemplateSourceFactory
from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate
from configTemplate.template.jsonConfigTemplateFactory import JSONConfigTemplateFactory
from configTemplate.template.defaultTemplateDefinition import DefaultTemplateDefinition

class testMultipleInheritenceEnvironment(TestCase):

    logging.basicConfig(filename='testing.log', level=logging.DEBUG)

    def testMultipleInheritence(self):
        
        importSource1=DirectoryTemplateImportSource(directoryPath=EXAMPLE_TEMPLATE_DIR, factoryMethod=JSONFileConfigTemplateSourceFactory)
        importSource2=DirectoryTemplateImportSource(directoryPath=EXAMPLE_COMMON_TEMPLATE_DIR, factoryMethod=JSONFileConfigTemplateSourceFactory)

        importSources = [importSource1, importSource2]

        env = DefaultEnvironment(importSource=importSources,
                                 templateFactory=JSONConfigTemplateFactory(),
                                 templateDefinition=DefaultTemplateDefinition())
        self.assertIsNotNone(env, 'Environment is None')

        template = env.getTemplate(MULTIPLE_INHERITANCE_JSON_TEMPLATE_NAME)
        self.assertTrue(template is not None, 'Template from environment is none!')

        renderedTemplate = template.render()
        print(renderedTemplate)