from unittest import TestCase

from configTemplate.template.jsonTemplateDefinition import JSONTemplateDefinition

class TestJSONTemplateDefinition(TestCase):

    def testGetTypeOfControlStructure(self):

        forLoopListControlStructure = [
            "{% for var in {{getVars}} %}",
            {},
            "{% endfor %}"
        ]        

        definition = JSONTemplateDefinition()

        controlStructureType = definition.getTypeOfControlStructure(forLoopListControlStructure)

        self.assertTrue(controlStructureType == JSONTemplateDefinition.CONTROL_STRUCTURE_TYPE_FOR)