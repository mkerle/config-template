
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))

EXAMPLE_TEMPLATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'exampleTemplates')
EXAMPLE_COMMON_TEMPLATE_DIR = os.path.join(EXAMPLE_TEMPLATE_DIR, 'common')
EXAMPLE_BASIC_TEMPLATE_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'basicJSONTemplate.json')
EXAMPLE_BASIC_MAIN_TEMPLATE_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'basicMainJSONTemplate.json')
EXAMPLE_BASIC_CHILD_TEMPLATE_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'basicChildJSONTemplate.json')
EXAMPLE_COMPLEX_MAIN_TEMPLATE_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'complexMainJSONTemplate.json')
EXAMPLE_COMPLEX_COMMON_INTERFACE_TEMPLATE_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'commonInterfaceSettings.json')
EXAMPLE_FOR_LOOP_TEMPLATE_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'forLoopJSONTemplate.json')

BASIC_JSON_TEMPLATE_NAME = 'Basic JSON Template'
BASIC_MAIN_JSON_TEMPLATE_NAME = 'Basic Main JSON Template'
BASIC_CHILD_JSON_TEMPLATE_NAME = 'Common Device Settings'
COMPLEX_MAIN_JSON_TEMPLATE_NAME = 'Complex Main JSON Template'
COMMON_INTERFACE_JSON_TEMPLATE_NAME = 'Common Interface Settings'
MULTIPLE_INHERITANCE_JSON_TEMPLATE_NAME = 'Main Multiple Inheritance Template'
FOR_LOOP_JSON_TEMPLATE_NAME = 'For Loop JSON Template'