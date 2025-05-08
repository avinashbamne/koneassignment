import yaml
from jinja2 import Environment, FileSystemLoader

def load_config():
    with open('blueprint/project-config.yml') as f:
        return yaml.safe_load(f)

def generate_ci(config):
    env = Environment(loader=FileSystemLoader('templates'))
    project = config['project']
    output = []

    # Add build steps
    for step in project['build_steps']:
        template = env.get_template(f"common/{step}.j2")
        output.append(template.render(project=project, language=project['language']))

    # Add language-specific setup
    lang_template = env.get_template(f"languages/{project['language']}.j2")
    output.append(lang_template.render(project=project))

    # Add deployment
    deploy_template = env.get_template(f"deployments/{project['deployment_method']}.j2")
    output.append(deploy_template.render(project=project))

    # Add branch/tag validation
    branch_list = "|".join(project['branch_strategy']['allowed_branches'])
    tag_pattern = project['branch_strategy']['tag_pattern']
    tag_template = env.get_template("common/tag-validation.j2")
    output.append(tag_template.render(branch_regex=branch_list, tag_pattern=tag_pattern))

    return "\n".join(output)

if __name__ == "__main__":
    config = load_config()
    pipeline = generate_ci(config)
    with open('output/.gitlab-ci.yml', 'w') as f:
        f.write(pipeline)
    print("Generated .gitlab-ci.yml in output/")


