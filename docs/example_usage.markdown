env = Environment(loader=JSONFileSystemLoader('./'))

template = env.get_template('myTemplate')

template.render(myVars)

def get_template(name):

	loader.update_cache()
	
	mainTemplate = loader.getTemplate(name)
	for inheritTemplate in mainTemplate.getInheritedTemplates():
		inheritedTemplates.append( {'name' : inheritTemplate.getName(), 'data' : inheritTemplate.getTemplate() } )
		
	return JSONTemplate(mainTemplate, inheritedTemplates)