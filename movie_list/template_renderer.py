import os

from jinja2 import Environment, FileSystemLoader, Template


def render(template_file, data):
    file_loader = FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'static'))
    jinja_env = Environment(loader=file_loader)
    template = jinja_env.get_template(template_file)
    return template.render(films=data)
