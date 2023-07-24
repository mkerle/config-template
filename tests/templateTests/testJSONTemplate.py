from unittest import TestCase

from tests.baseTest import BASIC_JSON_TEMPLATE_NAME, \
                            EXAMPLE_BASIC_TEMPLATE_PATH, \
                            EXAMPLE_TEMPLATE_DIR, \
                            EXAMPLE_BASIC_CHILD_TEMPLATE_PATH, \
                            EXAMPLE_BASIC_MAIN_TEMPLATE_PATH, \
                            BASIC_CHILD_JSON_TEMPLATE_NAME, \
                            BASIC_MAIN_JSON_TEMPLATE_NAME

from configTemplate.template.jsonConfigTemplate import JSONConfigTemplate
from configTemplate.template.jsonConfigTemplateFactory import JSONConfigTemplateFactory
from configTemplate.template.defaultTemplateDefinition import DefaultTemplateDefinition
from configTemplate.template.jsonConfigTemplateSource import JSONConfigTemplateSource
from configTemplate.template.jsonFileConfigTemplateSourceFactory import JSONFileConfigTemplateSourceFactory


class testJSONTemplate(TestCase):

    def createJSONTemplate(self):

        template = JSONConfigTemplate()

    def testCreateJSONTemplateFromSource(self):

        templateSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_BASIC_TEMPLATE_PATH)

        self.assertIsInstance(templateSource, JSONConfigTemplateSource)

        template = JSONConfigTemplateFactory.createTemplateFromSource(templateSource)
        self.assertIsInstance(template, JSONConfigTemplate)

        self.assertIsInstance(template.mainTemplateSource, JSONConfigTemplateSource)

    def _setupAndTestBasicInheritedTemplate(self):

        templateSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_BASIC_MAIN_TEMPLATE_PATH)
        self.assertIsInstance(templateSource, JSONConfigTemplateSource)

        inheritedSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_BASIC_CHILD_TEMPLATE_PATH)
        self.assertIsInstance(inheritedSource, JSONConfigTemplateSource)

        template = JSONConfigTemplateFactory.createTemplateFromSource(templateSource, {BASIC_CHILD_JSON_TEMPLATE_NAME : inheritedSource})

        self.assertIsInstance(template.mainTemplateSource, JSONConfigTemplateSource)
        self.assertIsInstance(template.inheritedTemplateSources, dict)
        self.assertIn(BASIC_CHILD_JSON_TEMPLATE_NAME, template.inheritedTemplateSources)
        self.assertIsInstance(template.inheritedTemplateSources[BASIC_CHILD_JSON_TEMPLATE_NAME], JSONConfigTemplateSource)

        return template


    def testCreateJSONTemplateWithInheritedSource(self):

        self._setupAndTestBasicInheritedTemplate()

    def testRenderJSONTemplateWithInheritedSource(self):

        expectedRenderedTemplate = {'device-settings': {'name': 'device1', 'mode': 'proxy', 'mem-size': '1024'}, 'flattern-test': {'some-list': ['a', 'b', 99, {'list-name': 'some-list-name', 'sub-list': ['foo', 'bar']}, ['69']], 'x': 'y'}}

        template = self._setupAndTestBasicInheritedTemplate()

        settings = {'name' : 'device1'}
        renderedTemplate = template.render(settings=settings)

        self.assertDictEqual(expectedRenderedTemplate, renderedTemplate, 'Rendered template is not as expected.')

        print(renderedTemplate)





