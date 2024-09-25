from dagger import JSON, Container, dag, function, object_type, Secret, File, Directory, DefaultPath, CacheVolume, Doc
from typing import Optional, Self, Annotated, Tuple


compileCode = """
from jinja2 import Environment, FileSystemLoader
import sys
import json

values = json.loads(sys.argv[1]) 

env = Environment(loader = FileSystemLoader('/templates'))
 
template = env.get_template('template.jinja')
 
with open("/output", 'w') as f:

    print(template.render(values), file = f)
"""


@object_type
class DaggerTemplates:
    """
    
    """

    @function
    def compile_template(
            self,
            json_values: Annotated[JSON, Doc("")],
            template_file: Annotated[File, Doc("")] 
        ) -> File:
        """

        """


        return (
            dag.container()
            .from_("python:3")
            .with_exec(["pip3", "install", "jinja2"])
            .with_new_file("/compile.py", compileCode)
            .with_mounted_file("/templates/template.jinja", template_file)
            .with_exec(["python", "/compile.py", json_values])
            .file("/output")
        )

