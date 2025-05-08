# 🔧 CI/CD Framework for Multi-Technology Projects

This project provides a **Jinja2-based CI/CD pipeline generator** that automatically produces a `.gitlab-ci.yml` file using a configurable blueprint. It supports a wide range of programming languages, build tools, and deployment methods in a modular and maintainable way.

---

## 🎯 Project Objective

To create a single GitLab/GitHub-based CI/CD framework that automatically generates standardized pipelines using a shared template or "blueprint" approach. It supports:

- Multiple programming languages: Python, Java, Node.js, etc.
- Diverse build types: pip, Maven, npm, etc.
- Deployment methods: Docker, CDK, CloudFormation, SAM, etc.
- Branching/tagging strategies: dev/staging/main + semantic versioning
- Modular template generation using **Jinja2**

---

## 🗂️ Folder Structure

```
ci-cd-framework/
├── blueprint/
│   └── project-config.yml        # YAML-based project blueprint
├── generator.py                  # Main script to render CI pipeline
├── output/
│   └── .gitlab-ci.yml            # Generated GitLab CI/CD pipeline
├── requirements.txt              # Python dependencies (Jinja2, PyYAML)
├── templates/                    # Modular template directory
│   ├── common/                   # Common CI steps (reusable)
│   │   ├── artifact-creation.j2
│   │   ├── ci-checks.j2
│   │   ├── code-analysis.j2
│   │   └── tag-validation.j2
│   ├── deployments/              # Deployment methods
│   │   └── docker.j2
│   └── languages/                # Language-specific setup
│       └── python.j2
```

---

## ⚙️ How It Works

1. You define a project using a YAML config file at `blueprint/project-config.yml`:

```yaml
project:
  name: "order-service"
  language: "python"
  build_tool: "pip"
  build_steps:
    - ci-checks
    - code-analysis
    - artifact-creation
  deployment_method: "docker"
  branch_strategy:
    allowed_branches:
      - dev
      - staging
      - main
    tag_pattern: "^v\d+\.\d+\.\d+$"
```

2. Run the generator script:
```bash
python generator.py
```

3. The system reads the YAML file and dynamically generates a `.gitlab-ci.yml` file in the `output/` folder using modular Jinja2 templates.

---

## 🧱 Template Types

- `common/`: Shared CI/CD stages like code analysis, artifact packaging, etc.
- `languages/`: Language-specific environment setup
- `deployments/`: Deployment logic (e.g., Docker build and push)

Each Jinja2 template receives the project config and renders its part of the pipeline.

---

## 🧪 Sample Output

```yaml
ci_checks:
  stage: test
  script:
    - echo "Running CI checks for python"

code_analysis:
  stage: test
  script:
    - pip install bandit
    - bandit -r .

artifact_creation:
  stage: package
  script:
    - python setup.py sdist bdist_wheel
    - ls dist/
  artifacts:
    paths:
      - dist/
      - target/

docker_deploy:
  stage: deploy
  script:
    - docker build -t order-service .
    - docker push your-docker-repo/order-service

validate_branch_and_tag:
  stage: validate
  script:
    - |
      echo "Validating branch and tag..."
      [[ "${CI_COMMIT_REF_NAME}" =~ ^(dev|staging|main)$ ]] || exit 1
      [[ -z "${CI_COMMIT_TAG}" || "${CI_COMMIT_TAG}" =~ ^v\d+\.\d+\.\d+$ ]] || exit 1
```

---

## 📦 Setup Instructions

1. Clone the repo and install dependencies:
```bash
pip install -r requirements.txt
```

2. Edit your YAML config under `blueprint/`.

3. Run:
```bash
python generator.py
```

---

## 🚀 Future Enhancements

- Add more templates for Java, Node.js, .NET, etc.
- Add testing stages (unit, integration)
- Add Terraform, SAM deployment options
- Support GitHub Actions workflow output

---

## 📜 License

MIT License

---

