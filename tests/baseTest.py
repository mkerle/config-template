
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))

EXAMPLE_TEMPLATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'exampleTemplates')
EXAMPLE_BASIC_TEMPLATE_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'basicJSONTemplate.json')
EXAMPLE_BASIC_MAIN_TEMPLATE_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'basicMainJSONTemplate.json')
EXAMPLE_BASIC_CHILD_TEMPLATE_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'basicChildJSONTemplate.json')

BASIC_JSON_TEMPLATE_NAME = 'Basic JSON Template'
BASIC_MAIN_JSON_TEMPLATE_NAME = 'Basic Main JSON Template'
BASIC_CHILD_JSON_TEMPLATE_NAME = 'Common Device Settings'