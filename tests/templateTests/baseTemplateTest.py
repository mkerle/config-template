
from tests.baseTest import EXAMPLE_TEMPLATE_DIR

import os

JSON_TEMPLATE_VALID_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'basicJSONTemplate.json')
JSON_TEMPLATE_INVALID_PATH = os.path.join(EXAMPLE_TEMPLATE_DIR, 'basicYAMLTemplate.yaml')

templateObj = {
    'name' : 'Test Template',
    'version' : 1,
    'template' : {
        
    }
}