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

    def testVariableModifier(self):

        variable = '{{myVar.getName|lower}}'

        definition = JSONTemplateDefinition()

        self.assertTrue(definition.hasTemplateVariable(variable))
        self.assertTrue(definition.hasTemplateVariableModifier(variable))

        varName, modifiers, origStr = definition.getTemplateVariableParts(variable)
        
        self.assertTrue(varName == 'myVar.getName')
        self.assertListEqual(['lower'], modifiers)
        self.assertTrue('{{myVar.getName|lower}}' == origStr)

        complexVariable = 'foo_{{myVar.getName|upper}}_bar'

        self.assertTrue(definition.hasTemplateVariable(complexVariable))
        self.assertTrue(definition.hasTemplateVariableModifier(complexVariable))

        varName, modifiers, origStr = definition.getTemplateVariableParts(complexVariable)
        
        self.assertTrue(varName == 'myVar.getName')
        self.assertListEqual(['upper'], modifiers)
        self.assertTrue('{{myVar.getName|upper}}' == origStr)