env = Environment(loader=JSONFileSystemLoader('./'))

template = env.get_template('myTemplate')

template.render(myVars)

def get_template(name):

	loader.update_cache()
	
	mainTemplate = loader.getTemplate(name)
	for inheritTemplate in mainTemplate.getInheritedTemplates():
		inheritedTemplates.append( {'name' : inheritTemplate.getName(), 'data' : inheritTemplate.getTemplate() } )
		
	return JSONTemplate(mainTemplate, inheritedTemplates)

## Render Variable

def getVariableScopes(self):

    variableScopes = {}
    self._traverseTemplate(self.getTemplate(), self.addVarible, variableScopes)

def _traverseTemplate(self, callback, callbackData, *args, **kwargs):

    for k in self.getTemplate():
        if (type(k)

def render(self, *args, **kwargs):

    self._traverseTemplate(*args, **kwargs)

def renderVariable(self, varName, varValue, *args, **kwargs):

    if ('.') in varValue:

        parts = varValue.split('.')

    if (parts[0] in kwargs):

        parent = kwargs[parts[0]]
        for subItem in range(1, len(parts)):
            if (parent.__get_item(parts[subItem]) is None):
                raise Exception('Could not resolve variable')

    if (is_callable(kwargs[varValue])):
        return kwargs[varValue]

    else:
        return parent

        


## Example Template

{
    "name" : "Template Name",
    "version" : 1,
    "inherited-templates" : [ { "Interface Template", "version" : 1 } ],
    "template" : {
        "$_var_deviceName" : "test device",
        "interfaces" : [
            {
                "vdom" : "vd-test",
                "interfaces" : [
                    {
                        "$_var_zoneName" : "DMZ",
                        "$_block_includes" : [ 'layer3LanInterface' ]
                        "name" : "{{device.getInterfaceName}},
                        "ip" : "{{device.getInterfaceIP}}"
                    }
                ]
            }
        ]
    }
}