from unittest import TestCase
import json

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
                            EXAMPLE_FOR_LOOP_LIST_COMPLEX_TEMPLATE_PATH, \
                            EXAMPLE_BASE_TEMPLATE_1_PATH, \
                            COMMON_BASE_TEMPLATE_1, \
                            EXAMPLE_FOR_LOOP_INLINE_TEMPLATE_PATH, \
                            FOR_LOOP_INLINE_TEMPLATE_NAME

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

        expectedRenderedTemplate = {'device-settings': {'name': 'device1', 'mode': 'proxy', 'logging': {'remote-server1': '192.168.254.253'}, 'mem-size': '1024'}, 'flattern-test': {'some-list': ['a', 'b', 99, {'list-name': 'some-list-name', 'sub-list': ['foo', 'bar']}, ['69']], 'x': 'y'}}

        template = self._setupAndTestBasicInheritedTemplate()

        settings = {'name' : 'device1'}
        renderedTemplate = template.render(settings=settings)

        #print(renderedTemplate)

        self.assertDictEqual(expectedRenderedTemplate, renderedTemplate, 'Rendered template is not as expected.')
        

    def testRenderComplexTemplate(self):

        templateSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_COMPLEX_MAIN_TEMPLATE_PATH)

        inheritedInterfaceSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_COMPLEX_COMMON_INTERFACE_TEMPLATE_PATH)
        inheritedDeviceSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_BASIC_CHILD_TEMPLATE_PATH)

        template = JSONConfigTemplateFactory.createTemplateFromSource(templateSource, {COMMON_INTERFACE_JSON_TEMPLATE_NAME : inheritedInterfaceSource, BASIC_CHILD_JSON_TEMPLATE_NAME : inheritedDeviceSource})

        renderedTemplate = template.render(settings=DeviceSettings('device2'))

        #print(renderedTemplate)

        expectedResult = {'device-settings': {'name': 'device2', 'mode': 'proxy', 'logging': {'remote-server2': '192.168.255.253', 'remote-server1': '192.168.254.253'}, 'mem-size': '1024'}, 'device-interfaces': [{'port': 'port1', 'vrf': 'DMZ', 'vlan': 100, 'name': 'DMZ-v100', 'mtu': 1500, 'vrrp-priority': 95, 'vrrp-dst': "'2.2.2.2'"}, {'port': 'port1', 'vrf': 'DMZ', 'vlan': 101, 'name': 'DMZ-v101', 'mtu': 1500, 'vrrp-priority': 95, 'vrrp-dst': "'2.2.2.2'"}, {'port': 'port1', 'vrf': 'CORP', 'vlan': 200, 'name': 'CORP-v200', 'mtu': 1500, 'vrrp-priority': 95, 'vrrp-dst': "'2.2.2.2'"}]}
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
        inheritedTemplateSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_BASE_TEMPLATE_1_PATH)
        inlineForLoopSource = JSONFileConfigTemplateSourceFactory.createTemplateSource(EXAMPLE_FOR_LOOP_INLINE_TEMPLATE_PATH)

        importedTemplates = {
            COMMON_BASE_TEMPLATE_1 : inheritedTemplateSource,
            FOR_LOOP_INLINE_TEMPLATE_NAME : inlineForLoopSource
        }

        template = JSONConfigTemplateFactory.createTemplateFromSource(templateSource, importedTemplates, JSONTemplateDefinition())        

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
            
            def getOtherData(self, xpath, flatternedTemplate, *args, **kwargs) -> list:

                return [ ChildObj('objectA', [{'id' : 'abc'}]), ChildObj('objectB', [{'id' : 'asdf'}, {'id': 'xyz'}]), ChildObj('objectC', []) ]

        renderedTemplate = template.render(config=TemplateObj())
        
        #print(renderedTemplate)
        expectedResult = {'some-list': [{'name': 'object1', 'members': [1], 'common-template-1': {'type': 'common1'}}, {'name': 'object2', 'members': [123, 234], 'common-template-1': {'type': 'common1'}}, {'name': 'object3', 'members': [], 'common-template-1': {'type': 'common1'}}, {'name': 'objectA', 'members': ['abc'], 'common-template-1': {'type': 'common1'}}, {'name': 'objectB', 'members': ['asdf', 'xyz'], 'common-template-1': {'type': 'common1'}}, {'name': 'objectC', 'members': [], 'common-template-1': {'type': 'common1'}}, {'name': 'object1', 'common-template-1': {'type': 'common1'}, 'import-member': [{'id': 1}]}, {'name': 'object2', 'common-template-1': {'type': 'common1'}, 'import-member': [{'id': 123}, {'id': 234}]}, {'name': 'object3', 'common-template-1': {'type': 'common1'}, 'import-member': []}, {'name': 'objectA', 'common-template-1': {'type': 'common1'}, 'import-member': [{'id': 'abc'}]}, {'name': 'objectB', 'common-template-1': {'type': 'common1'}, 'import-member': [{'id': 'asdf'}, {'id': 'xyz'}]}, {'name': 'objectC', 'common-template-1': {'type': 'common1'}, 'import-member': []}]}
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

        #print(renderedTemplate)

        expectedResult = {
            'emptyList' : [],
            'emptyListInAList' : [ [] ],
            'emptyDict' : {},
            'listWithEmptyDict' : [ {} ]
        }

        self.assertDictEqual(expectedResult, renderedTemplate)

    def testImportInForLoop(self):

        mainTemplateData = {
            "name" : "My Template",
            "version" : 1,
            "imports" : [ 
                { "name" : "Attrs 1" }
            ],
            "template" : {
                "address-objects" : [
                    {
                        "name" : "static_address_1",
                        "type" : "subnet",
                        "subnet" : "192.168.1.1"
                    },
                    [
                        "{% for obj in {{data}} %}",                        
                        "{% $_import_blocks [ 'Attrs 1' ] %}",                        
                        "{% endfor %}"
                    ]
                ]		
            }
        }

        attrTemplateData = {
            "name" : "Attrs 1",
            "version" : 1,
            "imports" : [],
            "template" : {
                "name" : "{{obj.getName}}",
                "type" : "subnet",
                "subnet" : "{{obj.getSubnet}}"
            }
        }

        class AddressData():

            def __init__(self, name, subnet):
                self.name = name
                self.subnet = subnet

            def getName(self, *args, **kwargs) -> str:
                return self.name
            
            def getSubnet(self, *args, **kwargs) -> str:
                return self.subnet
            
        sourceData = [AddressData("address_1", "10.1.1.1/32"), AddressData("address_2", "10.2.2.2/32")]

        mainTemplate = JSONConfigTemplateSource(mainTemplateData)
        attrTemplate = JSONConfigTemplateSource(attrTemplateData)

        template = JSONConfigTemplate(mainTemplate, { "Attrs 1" : attrTemplate }, JSONTemplateDefinition())

        renderedTemplate = template.render(data=sourceData)

        #print(renderedTemplate)

        expectedResult = {'address-objects': [{'name': 'static_address_1', 'type': 'subnet', 'subnet': '192.168.1.1'}, {'name': 'address_1', 'type': 'subnet', 'subnet': '10.1.1.1/32'}, {'name': 'address_2', 'type': 'subnet', 'subnet': '10.2.2.2/32'}]}

        self.assertDictEqual(expectedResult, renderedTemplate)

    def testForLoopControlStructureKwargs(self):

        mainTemplateData = {
            "name" : "My Template",
            "version" : 1,
            "imports" : [
                { "name" : "Variable Definition" }
            ],
            "template" : {
                "$_set" : {
                    "testIsNotRendered" : "This should not exist in the rendered output"
                },
                "addresses" : [
                    [
                        "{% for obj in {{data.getData}} kwargs=[ { 'template' : 'Variable Definition', 'variableXpath' : '$[var1]' }, { 'template' : 'Variable Definition', 'variableXpath' : '$[var2]' }, { 'template' : 'Variable Definition', 'variableXpath' : '$[var3]' }, { 'template' : 'Variable Definition', 'variableXpath' : '$[var4]' }, { 'template' : 'Variable Definition', 'variableXpath' : '$[Nested Variables][foo]' } ] %}",
                        {
                            "name" : "{{obj.getName}}",
                            "type" : "subnet",
                            "subnet" : "{{obj.getSubnet}}",
                            "custom-vars" : "{{obj.customVars}}"
                        },
                        "{% endfor %}"
                    ]
                ]
            }
        }

        kwargsData = {
            "name" : "Variable Definition",
            "version" : 1,
            "imports" : [ ],
            "template" : {
                "$_set" : {			
                    "var1" : { "value" : "somestring" },		
                    "var2" : { "value" : 1 },
                    "var3" : { "value" : [ 1000, 2000, 3000] },
                    "var4" : { "value" : { "myKey" : "{{data.getEnvironmentVar}}" } }
                },
                "Nested Variables" : {
                    "$_set" : {
                        "foo" : { "value" : "bar" }
                    }
                }
            }
        }

        class AddressData():

            def __init__(self, name, subnet):
                self.name = name
                self.subnet = subnet
                self.customVars = None

            def getName(self, *args, **kwargs) -> str:
                return self.name
            
            def getSubnet(self, *args, **kwargs) -> str:
                return self.subnet
            
        class SourceData():

            def __init__(self, addressData : list[AddressData]):

                self.addressData = addressData

            def getEnvironmentVar(self, *args, **kwargs) -> str:

                return 'default'

            def getData(self, xpath : str, flatternedTemplate : dict, *args, **kwargs):

                var1 = kwargs['var1']
                var2 = kwargs['var2']
                var3 = kwargs['var3']
                var4 = kwargs['var4']

                foo = kwargs['foo']

                for addr in self.addressData:
                    addr.customVars = {
                        'var1' : var1,
                        'var2' : var2,
                        'var3' : var3,
                        'var4' : var4,
                        'foo' : foo
                    }
                
                return self.addressData
            
        addresses = [AddressData("address_1", "10.1.1.1/32"), AddressData("address_2", "10.2.2.2/32")]
        sourceData = SourceData(addresses)

        mainTemplate = JSONConfigTemplateSource(mainTemplateData)        
        kwargsTemplate = JSONConfigTemplateSource(kwargsData)

        template = JSONConfigTemplate(mainTemplate, { "Variable Definition" : kwargsTemplate }, JSONTemplateDefinition())

        renderedTemplate = template.render(data=sourceData)

        #print(renderedTemplate)

        expectedResult = {'addresses': [{'name': 'address_1', 'type': 'subnet', 'subnet': '10.1.1.1/32', 'custom-vars': {'var1': 'somestring', 'var2': 1, 'var3': [1000, 2000, 3000], 'var4': {'myKey': 'default'}, 'foo': 'bar'}}, {'name': 'address_2', 'type': 'subnet', 'subnet': '10.2.2.2/32', 'custom-vars': {'var1': 'somestring', 'var2': 1, 'var3': [1000, 2000, 3000], 'var4': {'myKey': 'default'}, 'foo': 'bar'}}]}

        self.assertDictEqual(expectedResult, renderedTemplate)    

    def testMergeWithParent(self):

        importTemplateData = {
            "name" : "Child List Data",
            "version" : 1,
            "imports" : [],
            "template" : {
                "$_merge_list_with_parent" : [
                    {
                        "name" : "red"
                    },
                    {
                        "name" : "green"
                    },
                    {
                        "name" : "blue"
                    }
                ]
            }
        }

        templateData = {
            "name" : "Merge With Parent Basic Test",
            "version" : 1,
            "imports" : [ { "name" : "Child List Data" } ],
            "template" : {
                "colours" : [ { "$_import_blocks" : [ "Child List Data" ] } ]
            }
        }

        importedTemplateSource = JSONConfigTemplateSource(importTemplateData)
        templateSource = JSONConfigTemplateSource(templateData)

        template = JSONConfigTemplate(templateSource, { "Child List Data" : importedTemplateSource }, JSONTemplateDefinition())

        renderedTemplate = template.render()

        #print(renderedTemplate)

        expectedResult = {'colours': [{'name': 'red'}, {'name': 'green'}, {'name': 'blue'}]}

        self.assertDictEqual(expectedResult, renderedTemplate)

    def testMergeWithParentComplex(self):

        importTemplateData = {
            "name" : "Child List Data",
            "version" : 1,
            "imports" : [],
            "template" : {
                "$_merge_list_with_parent" : [
                    {
                        "name" : "red",
                        "value" : "{{data.red}}"
                    },
                    {
                        "name" : "green",
                        "value" : "{{data.green}}"
                    },
                    {
                        "name" : "blue",
                        "value" : "{{data.blue}}"
                    }
                ]
            }
        }

        templateData = {
            "name" : "Merge With Parent Basic Test",
            "version" : 1,
            "imports" : [ { "name" : "Child List Data" } ],
            "template" : {
                "colours" : [ [ 1, 2, 3], {}, { "$_import_blocks" : [ "Child List Data" ] }, "a", "b", "c" ]
            }
        }

        importedTemplateSource = JSONConfigTemplateSource(importTemplateData)
        templateSource = JSONConfigTemplateSource(templateData)

        template = JSONConfigTemplate(templateSource, { "Child List Data" : importedTemplateSource }, JSONTemplateDefinition())

        renderedTemplate = template.render(data={'red' : 100, 'green' : 200, 'blue' : 300})

        #print(renderedTemplate)

        expectedResult = {'colours': [[1, 2, 3], {}, 'a', 'b', 'c', {'name': 'red', 'value': 100}, {'name': 'green', 'value': 200}, {'name': 'blue', 'value': 300}]}

        self.assertDictEqual(expectedResult, renderedTemplate)

    def testMergeWithParentComplex2(self):

        importTemplateData1 = {
            "name" : "Child List Data",
            "version" : 1,
            "imports" : [],
            "template" : {
                "$_merge_list_with_parent" : [
                    {
                        "name" : "red",
                        "value" : "{{data.red}}"
                    },
                    {
                        "name" : "green",
                        "value" : "{{data.green}}"
                    },
                    {
                        "name" : "blue",
                        "value" : "{{data.blue}}"
                    }
                ]
            }
        }

        importTemplateData2 = {
            "name" : "Other Colours",
            "version" : 1,
            "imports" : [],
            "template" : {                
                "$_merge_list_with_parent" : [
                    {
                        "name" : "purple"
                    },
                    {
                        "name" : "black"
                    },
                    {
                        "name" : "white"
                    }
                ]                
            }
        }

        templateData = {
            "name" : "Merge With Parent Basic Test",
            "version" : 1,
            "imports" : [ { "name" : "Child List Data" } ],
            "template" : {
                "colours" : [ [ 1, 2, 3], {}, { "$_import_blocks" : [ "Child List Data", "Other Colours" ] }, "a", "b", "c" ]
            }
        }

        importedTemplateSource1 = JSONConfigTemplateSource(importTemplateData1)
        importedTemplateSource2 = JSONConfigTemplateSource(importTemplateData2)
        templateSource = JSONConfigTemplateSource(templateData)

        template = JSONConfigTemplate(templateSource, { "Child List Data" : importedTemplateSource1, "Other Colours" : importedTemplateSource2 }, JSONTemplateDefinition())

        renderedTemplate = template.render(data={'red' : 100, 'green' : 200, 'blue' : 300})

        #print(renderedTemplate)

        expectedResult = {'colours': [[1, 2, 3], {}, 'a', 'b', 'c', {'name': 'red', 'value': 100}, {'name': 'green', 'value': 200}, {'name': 'blue', 'value': 300}, {'name': 'purple'}, {'name': 'black'}, {'name': 'white'}]}

        self.assertDictEqual(expectedResult, renderedTemplate)

