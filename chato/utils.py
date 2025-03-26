from jinja2 import Environment, FileSystemLoader
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def render_template(template_name, **context):
    """Render a Jinja2 template with context"""
    template = jinja_env.get_template(template_name)
    return template.render(context)
