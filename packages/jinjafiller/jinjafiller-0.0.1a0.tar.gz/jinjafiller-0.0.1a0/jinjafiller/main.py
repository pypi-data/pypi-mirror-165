import jinja2
import json
import os

from .cla import get_cla


def main():
    args = get_cla().parse_args()

    CONFIG_PATH = args.config
    TEMPLATE_PATH = args.template
    OUTPUT_PATH = args.output

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    with open(TEMPLATE_PATH, "r") as f:
        template = f.read()

    template_obj = jinja2.Template(template)
    rendered_template = template_obj.render(config)
    rendered_template = os.linesep.join([s for s in rendered_template.splitlines() if s.strip()])

    with open(OUTPUT_PATH, "w") as f:
        f.write(rendered_template)