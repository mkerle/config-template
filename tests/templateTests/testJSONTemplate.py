from unittest import TestCase

from tests.baseTest import BASIC_JSON_TEMPLATE_NAME, \
                            EXAMPLE_BASIC_TEMPLATE_PATH, \
                            EXAMPLE_TEMPLATE_DIR, \
                            EXAMPLE_BASIC_CHILD_TEMPLATE_PATH, \
                            EXAMPLE_BASIC_MAIN_TEMPLATE_PATH, \
                            BASIC_CHILD_JSON_TEMPLATE_NAME, \
                            BASIC_MAIN_JSON_TEMPLATE_NAME, \
                            EXAMPLE_COMPLEX_MAIN_TEMPLATE_PATH, \
                            EXAMPLE_COMPLEX_COMMON_INTERFACE_TEMPLATE_PATH, \
                            COMMON_INTERFACE_JSON_TEMPLATE_NAME, \
                            FOR_LOOP_JSON_TEMPLATE_NAME, \
                            EXAMPLE_FOR_LOOP_TEMPLATE_PATH, \
                            EXAMPLE_FOR_LOOP_LIST_TEMPLATE_PATH, \
                            FOR_LOOP_LIST_JSON_TEMPLATE_NAME, \
                            EXAMPLE_FOR_LOOP_LIST_COMPLEX_TEMPLATE_PATH

from configTemplate.template.jsonConfigTemplate import JSONConfigTemplate
from configTemplate.template.jsonConfigTemplateFactory import JSONConfigTemplateFactory
from configTemplate.template.defaultTemplateDefinition import DefaultTemplateDefinition
from configTemplate.template.jsonTemplateDefinition import JSONTemplateDefinition
from configTemplate.template.jsonConfigTemplateSource import JSONConfigTemplateSource
from configTemplate.template.jsonFileConfigTemplateSourceFactory import JSONFileConfigTemplateSourceFactory

from tests.templateTests.complexJSONTestClass import DeviceSettings

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
        self.assertIsInstance(template.importedTemplatesSources, dict)
        self.assertIn(BASIC_CHILD_JSON_TEMPLATE_NAME, template.importedTemplatesSources)
        self.assertIsInstance(template.importedTemplatesSources[BASIC_CHILD_JSON_TEMPLATE_NAME], JSONConfigTemplateSource)

        return template


    def testCreateJSONTemplateWithInheritedSource(self):

        self._setupAndTestBasicInheritedTemplate()

    def testRenderJSONTemplateWithInheritedSource(self):

        expectedRenderedTemplate = {'device-settings': {'name': 'device1', 'mode': 'proxy', 'mem-size': '1024'}, 'flattern-test': {'some-list': ['a', 'b', 99, {'list-name': 'some-list-name', 'sub-list': ['foo', 'bar']}, ['69']], 'x': 'y'}}

        template = self._setupAndTestBasicInheritedTemplate()

        settings = {'name' : 'device1'}
        renderedTemplate = template.render(settings=settings)

        self.assertDictEqual(expectedRenderedTemplate, renderedTemplate, 'Rendered template is not as expected.')
        

    def testRenderComplexTemplate(self):

        templateSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_COMPLEX_MAIN_TEMPLATE_PATH)

        inheritedInterfaceSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_COMPLEX_COMMON_INTERFACE_TEMPLATE_PATH)
        inheritedDeviceSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_BASIC_CHILD_TEMPLATE_PATH)

        template = JSONConfigTemplateFactory.createTemplateFromSource(templateSource, {COMMON_INTERFACE_JSON_TEMPLATE_NAME : inheritedInterfaceSource, BASIC_CHILD_JSON_TEMPLATE_NAME : inheritedDeviceSource})

        renderedTemplate = template.render(settings=DeviceSettings('device2'))

        expectedResult = {'device-settings': {'name': 'device2', 'mode': 'proxy', 'mem-size': '1024'}, 'device-interfaces': [{'port': 'port1', 'vrf': 'DMZ', 'vlan': 100, 'name': 'DMZ-v100', 'mtu': 1500, 'vrrp-priority': 95, 'vrrp-dst': "'2.2.2.2'"}, {'port': 'port1', 'vrf': 'DMZ', 'vlan': 101, 'name': 'DMZ-v101', 'mtu': 1500, 'vrrp-priority': 95, 'vrrp-dst': "'2.2.2.2'"}, {'port': 'port1', 'vrf': 'CORP', 'vlan': 200, 'name': 'CORP-v200', 'mtu': 1500, 'vrrp-priority': 95, 'vrrp-dst': "'2.2.2.2'"}]}
        self.assertDictEqual(expectedResult, renderedTemplate)

    def testForLoopTemplate(self):

        templateSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_FOR_LOOP_TEMPLATE_PATH)

        template = JSONConfigTemplateFactory.createTemplateFromSource(templateSource, {}, JSONTemplateDefinition())

        renderedTemplate = template.render(myData=[{'name' : 'object1'}, {'name' : 'object2'}, {'name' : 'object3'}])
        
        expectedResult = {'some-list': [{'name': 'object1'}, {'name': 'object2'}, {'name': 'object3'}]}
        self.assertDictEqual(expectedResult, renderedTemplate)

    def testForLoopListTemplate(self):

        templateSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_FOR_LOOP_LIST_TEMPLATE_PATH)

        template = JSONConfigTemplateFactory.createTemplateFromSource(templateSource, {}, JSONTemplateDefinition())

        renderedTemplate = template.render(myData=[{'name' : 'object1'}, {'name' : 'object2'}, {'name' : 'object3'}])
        
        expectedResult = {'some-list': [{'name': 'object1'}, {'name': 'object2'}, {'name': 'object3'}]}
        self.assertDictEqual(expectedResult, renderedTemplate)

    def testForLoopListTemplateWithObject(self):

        templateSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_FOR_LOOP_LIST_COMPLEX_TEMPLATE_PATH)

        template = JSONConfigTemplateFactory.createTemplateFromSource(templateSource, {}, JSONTemplateDefinition())

        class ChildObj(object):

            def __init__(self, name : str, ids : list[dict]):
                self.name = name
                self.ids = ids

            def getName(self, xpath, flatternedTemplate, *args, **kwargs) -> str:

                return self.name

            def getMembers(self, xpath, flatternedTemplate, *args, **kwargs) -> list:

                return self.ids

        class TemplateObj(object):

            def getData(self, xpath, flatternedTemplate, *args, **kwargs) -> list:

                return [ ChildObj('object1', [{'id' : 1}]), ChildObj('object2', [{'id' : 123}, {'id':234}]), ChildObj('object3', []) ]

        renderedTemplate = template.render(config=TemplateObj())
        
        expectedResult = {'some-list': [{'name': 'object1', 'members': [1]}, {'name': 'object2', 'members': [123, 234]}, {'name': 'object3', 'members': []}]}
        self.assertDictEqual(expectedResult, renderedTemplate)        

    def testEdgeCaseTemplates(self):

        templateData = {
            'name' : 'Edge Case Test',
            'version' : 1,
            'imports' : [],
            'template' : {
                'emptyList' : [],
                'emptyListInAList' : [ [] ],
                'emptyDict' : {},
                'listWithEmptyDict' : [ {} ]
            }
        }
        templateSource = JSONConfigTemplateSource(templateData)

        template = JSONConfigTemplateFactory.createTemplateFromSource(templateSource, {}, JSONTemplateDefinition())

        renderedTemplate = template.render()

        print(renderedTemplate)

        expectedResult = {
            'emptyList' : [],
            'emptyListInAList' : [ [] ],
            'emptyDict' : {},
            'listWithEmptyDict' : [ {} ]
        }

        self.assertDictEqual(expectedResult, renderedTemplate)