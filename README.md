# What is this project?

The `configTemplate` python library provides a method of generating templates.  The library was primarily designed to handle templates using compliant JSON but can be expanded to handle other formats.

The project is similar in usage to Jinja2 but with the following differences:
- Templates can be written in compliant JSON - Jinja2 treats files as simple text files and therefore difficult to tell if your JSON has errors until it is rendered.
- `configTemplate` can handle multiple imports within a single template source.  Jinja2 is limited to a single import (inheritance) and is limited in usage of that import (can only be inserted once).
- Templates are referenced by a `name` rather than the filename or path.

# Features

The library is still under development but has the following features:
- import other template sources
- `if` control structures
- `for` loop control structures
- define variables within the template to provide hints to template rendering


# Installation

Using `pip`:

```
pip install git+https://github.com/mkerle/config-template.git
```

Download wheel (for install on offline systems):

```
pip wheel git+https://github.com/mkerle/config-template.git
```

# Basic Usage

To use the `configTemplate` library we need a few imports.  Focusing on JSON templates we need to import:

```python
from configTemplate.environment.defaultEnvironment import DefaultEnvironment
from configTemplate.importSource.directoryTemplateImportSource import DirectoryTemplateImportSource
from configTemplate.template.jsonFileConfigTemplateSourceFactory import JSONFileConfigTemplateSourceFactory
from configTemplate.template.jsonConfigTemplateFactory import JSONConfigTemplateFactory
from configTemplate.template.jsonTemplateDefinition import JSONTemplateDefinition
```

We then need to define where we are going to import our JSON template sources from using the `DirectoryTemplateImportSource` module.  The constructor takes a path to the template sources and a Factory class that will be used to create `JSONConfigTemplateSource` objects.

```python
importSource = DirectoryTemplateImportSource('./path/to/my/templates', JSONFileConfigTemplateSourceFactory)
```

With our `importSource` we can create a template environment using `DefaultEnvironment`.  The environment takes the import source, a Factory method to create templates (`JSONConfigTemplate`) as well as a template definition (`JSONTemplateDefinition`).

```python
env = DefaultEnvironment(importSource=importSources,
                            templateFactory=JSONConfigTemplateFactory,
                            templateDefinition=JSONTemplateDefinition())
```

We can now get our template object from the environment using the `name` of the template.

```python
template = env.getTemplate('My Template Name')
```

Finially we can render the template by specifiying arguments to help generate the final template.

```python
renderedTemplate = template.render(name='foo', someVar='bar')
```

# Basic JSON Template Structure

A JSON template source must define 3 fields:
1. The template `name`
1. The template `version`
1. The `template` body

A template can optionally define the `imports` field that defines the names of templates that will be used when rendering.

The basic structure is:

```json
{
    "name" : "My Template Name",
    "version" : 1,
    "imports" : [
        { "name" : "Some Other Template" }
    ],
    "template" : {
        "name" : "myDevice",        
        "ip" : "192.168.1.100/24",
        "gateway" : "192.168.1.1"
    }
}
```

# Defining variables in a template

Using the `DefaultTemplateDefinition` a variable can be defined using double curly braces surrounding the variable.

In a JSON template the variable will be defined as the value of a key in a `dict` or simply as a value in a list.  The variable should be defined as a `str` and therefore enclosed in quotes.

Examples:

```json
...
"template" : {
    ...
    "ip" : "{{ip}}",
    "users" : [ "root", "{{readOnlyUser}}" ]
    ...
}
```

To render the variables we can pass in named arguments to `render()` like below:

```python
template.render(ip='192.168.1.100', readOnlyUser='ro-user')
```

# Template Control Structures

Control structures can be defined in a `str` using the start and end tags as defined in the tmplate definition.  In the `DefaultTemplateDefinition` the start and end tags are `{%`, `%}` respectively.


## Conditional if Statements

`if` statements can be defined in a simalar way to variables.  The `if` statement should be defined in a string and has the format:

```
{% if condition then true_expression else false_expression %}
```

`condition` should be a variable supplied as an argument to the `render()` function without the double curly braces `{{` and `}}`.

Both `true_expression` and `false_expression` can define literals or variables.  If defining a variable it must use the double curly braces to ensure it gets intrepreted correctly.

## For Loops

`for` loop statements can be defined within `list` objects in a template.  The `for` loop should be defined in a string has the format:

```
{% for loopVariable in dataSource do returnValExpression %}
```

`loopVariable` is the name assigned to each element of the collection `dataSource`.  `dataSource` can be a literal expression or can obtained from the `render()` arguments by using curly braces.  `loopVariable` does not require the use of curly braces when used in the `returnValExpression` statement.

An example use of a for loop could be:

```json
...
interfaceNames : [
    "{% for interfaceObj in {{device.getInterfaces}} do interfaceObj.name %}"
]
```

When using JSON templates and the `JSONTemplateDefinition` there is an additional way to define for loops which is useful repeating structured data.  This for loop needs to be defined in a list where the 1st element must define the for loop and the last element indicates the end of the loop.  Any elements between the 1st and last elements will be repeated for each data source returned.  This method of for loop supports nested loops and variables (if using nesting be sure to take care with loop variable names).  Import of templates is supported inside the for loop structure.

An example of this for loop is shown below:

```json
"some-list" : [
    [
        "{% for data in {{config.getData}} %}",
        {
            "name" : "{{data.getName}}",
            "members" : [
                [
                    "{% for obj in {{data.getMembers}} %}",
                    "{{obj.id}}",
                    "{% endfor %}"
                ]
            ],
            "$_import_blocks" : [ "Common Template 1" ]
        },
        "{% endfor %}"
    ]
]
```

# Other Built-in Functions

Details of other built-in functions are described in the table below.


| Built-in | Description | Usage |
|----------| ------------|-------|
| `$_merge_list_with_parent` | The use of this bult-in is useful in JSON templates where a child template that is imported needs to merge with an existing list in order to maintain properly defined JSON documents.  In other template formats this built-in may not have any use or benifet. | `{ "$_merge_list_with_parent" : [ "the", "list", "data", "to", "merge" ] }`


# Using Imported Templates

To use imported templates we need to ensure:
1. The template source can be found by the template `environment`.
1. We include the template source `name` in the `imports` field.
1. We use the `$_import_blocks` keyword to define where the imported template(s) will be inserted.

A simple example:

`managementInterface.json`

```json
{
    "name" : "Management Interface",
    "version" : 1,
    "imports" : [],
    "template" : {
        "ip" : "{{settings.managementIP}}",
        "vlan" : 100,
        "type" : "management"
    }
}
```

`device.json`

```json
{
    "name" : "Device Template",
    "version" : 1,
    "imports" : [
        { "name" : "Management Interface" }
    ],
    "template" : {
        "name" : "myDevice",
        "port-1" : {
            "$_import_blocks" : [ "Management Interface" ]
        }
    }
}
```

This will produce a rendered template of:

```json
{
    "name" : "myDevice",
    "port-1": {
        "ip" : "192.168.1.99",
        "vlan" : 100,
        "type" : "management"
    }
}
```

With JSON templates we can import in two ways:

1. We can import inside of a dictionary object using `$_import_blocks` as the key and the value a list of template names to import.
1. We can import inside of a list where a `str` value uses the control structure syntax.  The syntax would look like: `{% $_import_blocks ['Import Template 1', 'Import Template 2'] %}`

