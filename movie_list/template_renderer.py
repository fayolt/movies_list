import os

from jinja2 import Environment, FileSystemLoader, Template


def render(template_dir, template_file, **kwargs):
    file_loader = FileSystemLoader(template_dir)
    jinja_env = Environment(loader=file_loader)
    template = jinja_env.get_template(template_file)
    return template.render(**kwargs)
