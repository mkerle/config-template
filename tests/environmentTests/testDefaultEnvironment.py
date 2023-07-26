from unittest import TestCase

from tests.baseTest import EXAMPLE_TEMPLATE_DIR, \
                            BASIC_JSON_TEMPLATE_NAME, \
                            COMPLEX_MAIN_JSON_TEMPLATE_NAME

from tests.templateTests.complexJSONTestClass import DeviceSettings

from configTemplate.environment.defaultEnvironment import DefaultEnvironment
from configTemplate.importSource.directoryTemplateImportSource import DirectoryTemplateImportSource
from configTemplate.template.jsonFileConfigTemplateSourceFactory import JSONFileConfigTemplateSourceFactory
from configTemplate.template.abstractConfigTemplate import AbstractConfigTemplate
from configTemplate.template.jsonConfigTemplateFactory import JSONConfigTemplateFactory
from configTemplate.template.defaultTemplateDefinition import DefaultTemplateDefinition

class testDefaultEnvironment(TestCase):

    def testInstantiateEnvironment(self):

        importSource=DirectoryTemplateImportSource(directoryPath=EXAMPLE_TEMPLATE_DIR, factoryMethod=JSONFileConfigTemplateSourceFactory)
        env = DefaultEnvironment(importSource=importSource)
        self.assertIsNotNone(env, 'Environment is None')


    def testGetBasicTemplateFromEnvironment(self):

        importSource=DirectoryTemplateImportSource(directoryPath=EXAMPLE_TEMPLATE_DIR, factoryMethod=JSONFileConfigTemplateSourceFactory)
        env = DefaultEnvironment(importSource=importSource, templateFactory=JSONConfigTemplateFactory(), templateDefinition=DefaultTemplateDefinition())
        self.assertIsNotNone(env, 'Environment is None')

        template = env.getTemplate(BASIC_JSON_TEMPLATE_NAME)

        self.assertIsInstance(template, AbstractConfigTemplate)

    def testComplexTemplateFromEnvironment(self):

        importSource=DirectoryTemplateImportSource(directoryPath=EXAMPLE_TEMPLATE_DIR, factoryMethod=JSONFileConfigTemplateSourceFactory)
        env = DefaultEnvironment(importSource=importSource, templateFactory=JSONConfigTemplateFactory(), templateDefinition=DefaultTemplateDefinition())
        self.assertIsNotNone(env, 'Environment is None')

        template = env.getTemplate(COMPLEX_MAIN_JSON_TEMPLATE_NAME)
        self.assertIsInstance(template, AbstractConfigTemplate)

        renderedTemplate = template.render(settings=DeviceSettings('device2'))
        print(renderedTemplate)