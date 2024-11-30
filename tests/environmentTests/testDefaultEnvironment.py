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

        expectedResult = {'device-settings': {'name': 'device2', 'mode': 'proxy', 'logging': {'remote-server2': '192.168.255.253', 'remote-server1': '192.168.254.253'}, 'mem-size': '1024'}, 'device-interfaces': [{'port': 'port1', 'vrf': 'DMZ', 'vlan': 100, 'name': 'DMZ-v100', 'zone-lower': 'dmz', 'zone-lower-upper': 'DMZ', 'zone-start': 'DMZ-suffix', 'zone-end': 'zone-DMZ', 'zone-middle': 'zone-dmz-suffix', 'mtu': 1500, 'vrrp-priority': 95, 'vrrp-dst': "'2.2.2.2'"}, {'port': 'port1', 'vrf': 'DMZ', 'vlan': 101, 'name': 'DMZ-v101', 'zone-lower': 'dmz', 'zone-lower-upper': 'DMZ', 'zone-start': 'DMZ-suffix', 'zone-end': 'zone-DMZ', 'zone-middle': 'zone-dmz-suffix', 'mtu': 1500, 'vrrp-priority': 95, 'vrrp-dst': "'2.2.2.2'"}, {'port': 'port1', 'vrf': 'CORP', 'vlan': 200, 'name': 'CORP-v200', 'zone-lower': 'corp', 'zone-lower-upper': 'CORP', 'zone-start': 'CORP-suffix', 'zone-end': 'zone-CORP', 'zone-middle': 'zone-corp-suffix', 'mtu': 1500, 'vrrp-priority': 95, 'vrrp-dst': "'2.2.2.2'"}]}

        #print(renderedTemplate)

        self.assertDictEqual(expectedResult, renderedTemplate)

        