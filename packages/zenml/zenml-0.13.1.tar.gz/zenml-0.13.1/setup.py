# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zenml',
 'zenml.alerter',
 'zenml.annotators',
 'zenml.artifact_stores',
 'zenml.artifacts',
 'zenml.cli',
 'zenml.config',
 'zenml.container_registries',
 'zenml.data_validators',
 'zenml.entrypoints',
 'zenml.experiment_trackers',
 'zenml.feature_stores',
 'zenml.integrations',
 'zenml.integrations.airflow',
 'zenml.integrations.airflow.orchestrators',
 'zenml.integrations.aws',
 'zenml.integrations.aws.container_registries',
 'zenml.integrations.aws.secrets_managers',
 'zenml.integrations.aws.step_operators',
 'zenml.integrations.azure',
 'zenml.integrations.azure.artifact_stores',
 'zenml.integrations.azure.secrets_managers',
 'zenml.integrations.azure.step_operators',
 'zenml.integrations.dash',
 'zenml.integrations.dash.visualizers',
 'zenml.integrations.deepchecks',
 'zenml.integrations.deepchecks.data_validators',
 'zenml.integrations.deepchecks.materializers',
 'zenml.integrations.deepchecks.steps',
 'zenml.integrations.deepchecks.visualizers',
 'zenml.integrations.evidently',
 'zenml.integrations.evidently.data_validators',
 'zenml.integrations.evidently.materializers',
 'zenml.integrations.evidently.steps',
 'zenml.integrations.evidently.visualizers',
 'zenml.integrations.facets',
 'zenml.integrations.facets.visualizers',
 'zenml.integrations.feast',
 'zenml.integrations.feast.feature_stores',
 'zenml.integrations.gcp',
 'zenml.integrations.gcp.artifact_stores',
 'zenml.integrations.gcp.orchestrators',
 'zenml.integrations.gcp.secrets_manager',
 'zenml.integrations.gcp.step_operators',
 'zenml.integrations.github',
 'zenml.integrations.github.orchestrators',
 'zenml.integrations.github.secrets_managers',
 'zenml.integrations.graphviz',
 'zenml.integrations.graphviz.visualizers',
 'zenml.integrations.great_expectations',
 'zenml.integrations.great_expectations.data_validators',
 'zenml.integrations.great_expectations.materializers',
 'zenml.integrations.great_expectations.steps',
 'zenml.integrations.great_expectations.visualizers',
 'zenml.integrations.huggingface',
 'zenml.integrations.huggingface.materializers',
 'zenml.integrations.kserve',
 'zenml.integrations.kserve.custom_deployer',
 'zenml.integrations.kserve.model_deployers',
 'zenml.integrations.kserve.secret_schemas',
 'zenml.integrations.kserve.services',
 'zenml.integrations.kserve.steps',
 'zenml.integrations.kubeflow',
 'zenml.integrations.kubeflow.metadata_stores',
 'zenml.integrations.kubeflow.orchestrators',
 'zenml.integrations.kubernetes',
 'zenml.integrations.kubernetes.metadata_stores',
 'zenml.integrations.kubernetes.orchestrators',
 'zenml.integrations.label_studio',
 'zenml.integrations.label_studio.annotators',
 'zenml.integrations.label_studio.label_config_generators',
 'zenml.integrations.label_studio.steps',
 'zenml.integrations.lightgbm',
 'zenml.integrations.lightgbm.materializers',
 'zenml.integrations.mlflow',
 'zenml.integrations.mlflow.experiment_trackers',
 'zenml.integrations.mlflow.model_deployers',
 'zenml.integrations.mlflow.services',
 'zenml.integrations.mlflow.steps',
 'zenml.integrations.neural_prophet',
 'zenml.integrations.neural_prophet.materializers',
 'zenml.integrations.pillow',
 'zenml.integrations.pillow.materializers',
 'zenml.integrations.plotly',
 'zenml.integrations.plotly.visualizers',
 'zenml.integrations.pytorch',
 'zenml.integrations.pytorch.materializers',
 'zenml.integrations.pytorch_lightning',
 'zenml.integrations.pytorch_lightning.materializers',
 'zenml.integrations.s3',
 'zenml.integrations.s3.artifact_stores',
 'zenml.integrations.scipy',
 'zenml.integrations.scipy.materializers',
 'zenml.integrations.seldon',
 'zenml.integrations.seldon.custom_deployer',
 'zenml.integrations.seldon.model_deployers',
 'zenml.integrations.seldon.secret_schemas',
 'zenml.integrations.seldon.services',
 'zenml.integrations.seldon.steps',
 'zenml.integrations.sklearn',
 'zenml.integrations.sklearn.materializers',
 'zenml.integrations.slack',
 'zenml.integrations.slack.alerters',
 'zenml.integrations.slack.steps',
 'zenml.integrations.spark',
 'zenml.integrations.spark.materializers',
 'zenml.integrations.spark.step_operators',
 'zenml.integrations.tekton',
 'zenml.integrations.tekton.orchestrators',
 'zenml.integrations.tensorboard',
 'zenml.integrations.tensorboard.services',
 'zenml.integrations.tensorboard.visualizers',
 'zenml.integrations.tensorflow',
 'zenml.integrations.tensorflow.materializers',
 'zenml.integrations.vault',
 'zenml.integrations.vault.secrets_manager',
 'zenml.integrations.wandb',
 'zenml.integrations.wandb.experiment_trackers',
 'zenml.integrations.whylogs',
 'zenml.integrations.whylogs.data_validators',
 'zenml.integrations.whylogs.materializers',
 'zenml.integrations.whylogs.secret_schemas',
 'zenml.integrations.whylogs.steps',
 'zenml.integrations.whylogs.visualizers',
 'zenml.integrations.xgboost',
 'zenml.integrations.xgboost.materializers',
 'zenml.io',
 'zenml.materializers',
 'zenml.metadata_stores',
 'zenml.model_deployers',
 'zenml.orchestrators',
 'zenml.orchestrators.local',
 'zenml.pipelines',
 'zenml.post_execution',
 'zenml.secret',
 'zenml.secret.schemas',
 'zenml.secrets_managers',
 'zenml.secrets_managers.local',
 'zenml.services',
 'zenml.services.local',
 'zenml.stack',
 'zenml.step_operators',
 'zenml.steps',
 'zenml.steps.step_interfaces',
 'zenml.utils',
 'zenml.visualizers',
 'zenml.zen_server',
 'zenml.zen_stores',
 'zenml.zen_stores.models']

package_data = \
{'': ['*']}

install_requires = \
['analytics-python>=1.4.0,<2.0.0',
 'apache-beam>=2.30.0,<3.0.0',
 'click-params>=0.3.0,<0.4.0',
 'click>=8.0.1,<9.0.0',
 'distro>=1.6.0,<2.0.0',
 'gitpython>=3.1.18,<4.0.0',
 'httplib2>=0.19.1,<0.20',
 'markupsafe==1.1.1',
 'ml-pipelines-sdk==1.8.0',
 'nbconvert==6.4.4',
 'pandas>=1.1.5,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pyparsing>=2.4.0,<3',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'rich[jupyter]>=12.0.0,<13.0.0',
 'sqlmodel>=0.0.6,<0.1.0']

extras_require = \
{'server': ['fastapi>=0.75.0,<0.76.0', 'uvicorn[standard]>=0.17.5,<0.18.0'],
 'stacks': ['python-terraform>=0.10.1,<0.11.0']}

entry_points = \
{'console_scripts': ['zenml = zenml.cli.cli:cli']}

setup_kwargs = {
    'name': 'zenml',
    'version': '0.13.1',
    'description': 'ZenML: Write production-ready ML code.',
    'long_description': '<!-- PROJECT SHIELDS -->\n<!--\n*** I\'m using markdown "reference style" links for readability.\n*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).\n*** See the bottom of this document for the declaration of the reference variables\n*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.\n*** https://www.markdownguide.org/basic-syntax/#reference-style-links\n-->\n\n[![PyPi][pypi-shield]][pypi-url]\n[![PyPi][pypiversion-shield]][pypi-url]\n[![PyPi][downloads-shield]][downloads-url]\n[![Contributors][contributors-shield]][contributors-url]\n[![License][license-shield]][license-url]\n[![Build][build-shield]][build-url]\n[![Interrogate][interrogate-shield]][interrogate-url]\n<!-- [![CodeCov][codecov-shield]][codecov-url] -->\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[pypi-shield]: https://img.shields.io/pypi/pyversions/zenml?style=for-the-badge\n[pypi-url]: https://pypi.org/project/zenml/\n[pypiversion-shield]: https://img.shields.io/pypi/v/zenml?style=for-the-badge\n\n[downloads-shield]: https://img.shields.io/pypi/dm/zenml?style=for-the-badge\n[downloads-url]: https://pypi.org/project/zenml/\n[codecov-shield]: https://img.shields.io/codecov/c/gh/zenml-io/zenml?style=for-the-badge\n[codecov-url]: https://codecov.io/gh/zenml-io/zenml\n[contributors-shield]: https://img.shields.io/github/contributors/zenml-io/zenml?style=for-the-badge\n[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors\n[license-shield]: https://img.shields.io/github/license/zenml-io/zenml?style=for-the-badge\n[license-url]: https://github.com/zenml-io/zenml/blob/main/LICENSE\n[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555\n[linkedin-url]: https://www.linkedin.com/company/zenml/\n[twitter-shield]: https://img.shields.io/twitter/follow/zenml_io?style=for-the-badge\n[twitter-url]: https://twitter.com/zenml_io\n[slack-shield]: https://img.shields.io/badge/-Slack-black.svg?style=for-the-badge&logo=linkedin&colorB=555\n[slack-url]: https://zenml.io/slack-invite\n[build-shield]: https://img.shields.io/github/workflow/status/zenml-io/zenml/Build,%20Lint,%20Unit%20&%20Integration%20Test/develop?logo=github&style=for-the-badge\n[build-url]: https://github.com/zenml-io/zenml/actions/workflows/ci.yml\n[interrogate-shield]: https://img.shields.io/badge/Interrogate-100%25-brightgreen?style=for-the-badge&logo=interrogate\n[interrogate-url]: https://interrogate.readthedocs.io/en/latest/\n\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n  <a href="https://zenml.io">\n    <img src="docs/book/assets/zenml_logo.png" alt="Logo" width="400">\n  </a>\n\n  <h3 align="center">Build portable, production-ready MLOps pipelines.</h3>\n\n  <p align="center">\n    A simple yet powerful open-source framework that scales your MLOps stack with your needs.\n    <br />\n    <a href="https://docs.zenml.io/"><strong>Explore the docs »</strong></a>\n    <br />\n    <div align="center">\n      Join our <a href="https://zenml.io/slack-invite" target="_blank">\n      <img width="25" src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/306_Slack-512.png" alt="Slack"/>\n    <b>Slack Community</b> </a> and be part of the ZenML family.\n    </div>\n    <br />\n    <a href="https://zenml.io/features">Features</a>\n    ·\n    <a href="https://zenml.io/roadmap">Roadmap</a>\n    ·\n    <a href="https://github.com/zenml-io/zenml/issues">Report Bug</a>\n    ·\n    <a href="https://zenml.io/discussion">Vote New Features</a>\n    ·\n    <a href="https://blog.zenml.io/">Read Blog</a>\n    ·\n    <a href="#-meet-the-team">Meet the Team</a>\n    <br />\n    🎉 Version 0.13.1 is out. Check out the release notes\n    <a href="https://github.com/zenml-io/zenml/releases">here</a>.\n    <br />\n    <br />\n    <a href="https://www.linkedin.com/company/zenml/">\n    <img src="https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555" alt="Logo">\n    </a>\n    <a href="https://twitter.com/zenml_io">\n    <img src="https://img.shields.io/badge/-Twitter-black.svg?style=for-the-badge&logo=twitter&colorB=555" alt="Logo">\n    </a>\n  </p>\n</div>\n\n<!-- TABLE OF CONTENTS -->\n<details>\n  <summary>🏁 Table of Contents</summary>\n  <ol>\n    <li>\n      <a href="#-why-zenml">Why ZenML?</a>\n    </li>\n    <li>\n    <a href="#-what-is-zenml">What is ZenML?</a>\n    </li>\n    <li>\n      <a href="#-getting-started">Getting Started</a>\n      <ul>\n        <li><a href="#-installation">Installation</a></li>\n        <li><a href="#-first-run">First run</a></li>\n        <li><a href="#-zenbytes">ZenBytes</a></li>\n        <li><a href="#-zenfiles">ZenFiles</a></li>\n      </ul>\n    </li>\n    <li><a href="#-collaborate-with-your-team">Collaborate with your team</a></li>\n    <li><a href="#-learn-more">Learn More</a></li>\n    <li><a href="#-roadmap">Roadmap</a></li>\n    <li><a href="#-contributing-and-community">Contributing and Community</a></li>\n    <li><a href="#-meet-the-team">Meet the Team</a></li>\n    <li><a href="#-getting-help">Getting Help</a></li>\n    <li><a href="#-license">License</a></li>\n  </ol>\n</details>\n\n<br />\n\n# 🤖 Why ZenML?\n\n🤹 Are you an ML engineer or data scientist shipping models to production and juggling a plethora of tools? \n\n🤷\u200d♂️ Do you struggle with versioning data, code, and models in your projects? \n\n👀 Have you had trouble replicating production pipelines and monitoring models in production?\n\n✅ If you answered yes to any of the above, ZenML is here to help with all that and more...\n\nEveryone loves to train ML models, but few talks about shipping them into production, and even fewer can do it well.\nAt ZenML, we believe the journey from model development to production doesn\'t need to be long and painful.\n\n![The long journey from experimentation to production.](docs/book/assets/1-pipeline-hard-reproduce.png)\n\n\nWith ZenML, you can concentrate on what you do best - developing ML models and not worry about infrastructure or deployment tools.\n\nIf you come from unstructured notebooks or scripts with lots of manual processes, ZenML will make the path to production easier and faster for you and your team.\nUsing ZenML allows you to own the entire pipeline - from experimentation to production.\n\nThis is why we built ZenML. Read more [here](https://blog.zenml.io/why-zenml/).\n\n\n\n\n# 💡 What is ZenML?\n\n<div align="center">\n    <img src="docs/book/assets/tailor.gif">\n</div>\n\n\nZenML is an extensible, open-source MLOps framework for creating portable, production-ready MLOps pipelines. It\'s built for Data Scientists, ML Engineers, and MLOps Developers to collaborate as they develop to production. \n\nZenML offers a simple and flexible syntax, is cloud- and tool-agnostic, and has interfaces/abstractions catered toward ML workflows. \nWith ZenML you\'ll have all your favorite tools in one place so you can tailor a workflow that caters to your specific needs.\n\n![ZenML unifies all your tools in one place.](docs/book/assets/sam-side-by-side-full-text.png)\n\nRead more on all tools you can readily use in the [integrations](https://zenml.io/integrations) section. Can\'t find your tool? You can always [write your own integration](https://docs.zenml.io/developer-guide/advanced-usage/custom-flavors) to use it with ZenML.\n\n# 🤸 Getting Started\n\n## 💾 Installation\n**Option 1** - Install ZenML via [PyPI](https://pypi.org/project/zenml/):\n\n```bash\npip install zenml\n```\n> **Note** - ZenML supports Python 3.7, 3.8, and 3.9.\n\n**Option 2** - If you’re feeling adventurous, try out the bleeding-edge installation:\n\n```bash\npip install git+https://github.com/zenml-io/zenml.git@develop --upgrade\n```\n\n> **Warning** - Fire dragons ahead. Proceed at your own risk!\n\n**Option 3** - Install via a Docker image hosted publicly on\n[DockerHub](https://hub.docker.com/r/zenmldocker/zenml):\n\n```shell\ndocker run -it zenmldocker/zenml /bin/bash\n```\n\n> **Warning** \n> #### Known installation issues for M1 Mac users\n>\n> If you have an M1 Mac machine and encounter an installation error, \n> try setting up `brew` and `pyenv` with Rosetta 2 and then install ZenML. The issue arises because some dependencies \n> aren’t fully compatible with the vanilla ARM64 Architecture. The following links may be helpful (Thank you @Reid Falconer) :\n>\n>- [Pyenv with Apple Silicon](http://sixty-north.com/blog/pyenv-apple-silicon.html)\n>- [Install Python Under Rosetta 2](https://medium.com/thinknum/how-to-install-python-under-rosetta-2-f98c0865e012)\n\n\n## 🏇 First run\n\nIf you\'re here for the first time, we recommend running:\n\n```shell\nzenml go\n```\n\nThis spins up a Jupyter notebook that walks you through various functionalities of ZenML at a high level.\n\nBy the end, you\'ll get a glimpse of how to use ZenML to:\n\n+ Train, evaluate, deploy, and embed a model in an inference pipeline.\n+ Automatically track and version data, models, and other artifacts.\n+ Track model hyperparameters and metrics with experiment tracking tools.\n+ Measure and visualize train-test skew, training-serving skew, and data drift.\n\n## 👨\u200d🍳 Open Source MLOps Stack Recipes\n\nZenML boasts a ton of [integrations](https://zenml.io/integrations) into popular MLOps tools. The [ZenML Stack](https://docs.zenml.io/developer-guide/stacks-profiles-repositories) concept ensures that these tools work nicely together, therefore bringing structure and standardization into the MLOps workflow.\n\nHowever, ZenML assumes that the stack infrastructure for these tools is already provisioned. If you do not have deployed infrastructure, and want to quickly spin up combinations of tools on the cloud, the [MLOps stack sister repository](https://github.com/zenml-io/mlops-stacks) contains a series of Terraform-based recipes to provision such stacks. These recipes can be used directly with ZenML:\n\n```bash\npip install zenml[stacks]\n\nzenml stack recipe deploy <NAME_OF_STACK_RECIPE> --import\n```\n\nThe above command not only provisions the given tools, but also automatically creates a ZenML stack with the configuration of the deployed recipe!\n\n## 🍰 ZenBytes\nNew to MLOps? Get up to speed by visiting the [ZenBytes](https://github.com/zenml-io/zenbytes) repo.\n\n>ZenBytes is a series of short practical MLOps lessons taught using ZenML. \n>It covers many of the [core concepts](https://docs.zenml.io/getting-started/core-concepts) widely used in ZenML and MLOps in general.\n\n## 📜 ZenFiles\nAlready comfortable with ZenML and wish to elevate your pipeline into production mode? Check out [ZenFiles](https://github.com/zenml-io/zenfiles).\n\n>ZenFiles is a collection of production-grade ML use-cases powered by ZenML. They are fully fleshed out, end-to-end projects that showcase ZenML\'s capabilities. They can also serve as a template from which to start similar projects.\n\n# 👭 Collaborate with your team\n\nZenML is built to support teams working together. \nThe underlying infrastructure on which your ML workflows run can be shared, as can the data, assets, and artifacts in your workflow. \n\nIn ZenML, a Stack represents a set of configurations for your MLOps tools and infrastructure. You can quickly share your ZenML stack with anyone by exporting the stack:\n\n```\nzenml stack export <STACK_NAME> <FILENAME.yaml>\n```\n\nSimilarly, you can import a stack by running:\n```\nzenml stack import <STACK_NAME> <FILENAME.yaml>\n```\n\nLearn more on importing/exporting stacks [here](https://docs.zenml.io/collaborate/stack-export-import).\n\n\nThe [ZenML Profiles](https://docs.zenml.io/collaborate/zenml-store) offer an easy way to manage and switch between your stacks. All your stacks, components, and other classes of ZenML objects can be stored in a central location and shared across multiple users, teams, and automated systems such as CI/CD processes.\n\nWith the [ZenServer](https://docs.zenml.io/collaborate/zenml-server) \nyou can deploy ZenML as a centralized service and connect entire teams and organizations to an easy-to-manage collaboration platform that provides a unified view of the MLOps processes, tools, and technologies that support your entire AI/ML project lifecycle.\n\nRead more about using ZenML for collaboration [here](https://docs.zenml.io/collaborate/collaborate-with-zenml).\n\n# 📖 Learn More\n\n| ZenML Resources | Description |\n| ------------- | - |\n| 🧘\u200d♀️ **[ZenML 101]** | New to ZenML? Here\'s everything you need to know! |\n| ⚛️ **[Core Concepts]** | Some key terms and concepts we use. |\n| 🚀 **[Our latest release]** | New features, bug fixes. |\n| 🗳 **[Vote for Features]** | Pick what we work on next! |\n| 📓 **[Docs]** | Full documentation for creating your own ZenML pipelines. |\n| 📒 **[API Reference]** | Detailed reference on ZenML\'s API. |\n| 🍰 **[ZenBytes]** | A guided and in-depth tutorial on MLOps and ZenML. |\n| 🗂️️ **[ZenFiles]** | End-to-end projects using ZenML. |\n| 👨\u200d🍳 **[MLOps Stacks]** | Terraform based infrastructure recipes for pre-made ZenML stacks. |\n| ⚽️ **[Examples]** | Learn best through examples where ZenML is used? We\'ve got you covered. |\n| 📬 **[Blog]** | Use cases of ZenML and technical deep dives on how we built it. |\n| 🔈 **[Podcast]** | Conversations with leaders in ML, released every 2 weeks. |\n| 📣 **[Newsletter]** | We build ZenML in public. Subscribe to learn how we work. |\n| 💬 **[Join Slack]** | Need help with your specific use case? Say hi on Slack! |\n| 🗺 **[Roadmap]** | See where ZenML is working to build new features. |\n| 🙋\u200d♀️ **[Contribute]** | How to contribute to the ZenML project and code base. |\n\n[ZenML 101]: https://docs.zenml.io/\n[Core Concepts]: https://docs.zenml.io/getting-started/core-concepts\n[API Guide]: https://docs.zenml.io/v/docs/developer-guide/steps-and-pipelines/functional-vs-class-based-api\n[Our latest release]: https://github.com/zenml-io/zenml/releases\n[Vote for Features]: https://zenml.io/discussion\n[Docs]: https://docs.zenml.io/\n[API Reference]: https://apidocs.zenml.io/\n[ZenBytes]: https://github.com/zenml-io/zenbytes\n[ZenFiles]: https://github.com/zenml-io/zenfiles\n[MLOps Stacks]: https://github.com/zenml-io/mlops-stacks\n[Examples]: https://github.com/zenml-io/zenml/tree/main/examples\n[Blog]: https://blog.zenml.io/\n[Podcast]: https://podcast.zenml.io/\n[Newsletter]: https://zenml.io/newsletter/\n[Join Slack]: https://zenml.io/slack-invite/\n[Roadmap]: https://zenml.io/roadmap\n[Contribute]: https://github.com/zenml-io/zenml/blob/main/CONTRIBUTING.md\n\n\n# 🗺 Roadmap\n\nZenML is being built in public. The [roadmap](https://zenml.io/roadmap) is a\nregularly updated source of truth for the ZenML community to understand where\nthe product is going in the short, medium, and long term.\n\nZenML is managed by a [core team](https://zenml.io/company#CompanyTeam) of developers that are\nresponsible for making key decisions and incorporating feedback from the\ncommunity. The team oversees feedback via various channels, and you can directly\ninfluence the roadmap as follows:\n\n- Vote on your most wanted feature on our [Discussion\n  board](https://zenml.io/discussion).\n- Start a thread in our [Slack channel](https://zenml.io/slack-invite).\n- [Create an issue](https://github.com/zenml-io/zenml/issues/new/choose) on our Github repo.\n\n\n\n# 🙌 Contributing and Community\n\nWe would love to develop ZenML together with our community! Best way to get\nstarted is to select any issue from the [`good-first-issue`\nlabel](https://github.com/zenml-io/zenml/labels/good%20first%20issue). If you\nwould like to contribute, please review our [Contributing\nGuide](CONTRIBUTING.md) for all relevant details.\n\n<br>\n\n![Repobeats analytics\nimage](https://repobeats.axiom.co/api/embed/635c57b743efe649cadceba6a2e6a956663f96dd.svg\n"Repobeats analytics image")\n\n\n# 👩\u200d👩\u200d👧\u200d👦 Meet the Team\n\n![Meet the Team](./docs/book/assets/meet_the_team.jpeg)\n\nHave a question that\'s too hard to express on our Slack? Is it just too much effort to say everything on a \nlong GitHub issue? Or are you just curious about what ZenML has been up to in the past week? Well, register now for the ZenML Office (Half) Hour to get your answers and more!\nIt\'s free and open to everyone.\n\nEvery week, part of the ZenML [core team](https://zenml.io/company#CompanyTeam) will pop in for 30 minutes to interact directly with the community. Sometimes we\'ll be presenting a feature. Other times we just take questions and have fun. Join us if you are curious about ZenML, or just want to talk shop about MLOps.\n\n\n\nWe will host the gathering every Wednesday 8:30AM PT (5:30PM CET). \nRegister now through [this link](https://www.eventbrite.com/e/zenml-meet-the-community-tickets-354426688767), \nor subscribe to the [public events calendar](https://calendar.google.com/calendar/u/0/r?cid=Y19iaDJ0Zm44ZzdodXBlbnBzaWplY3UwMmNjZ0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t) to get notified \nbefore every community gathering.\n\n# 🆘 Getting Help\n\nThe first point of call should be [our Slack group](https://zenml.io/slack-invite/).\nAsk your questions about bugs or specific use cases, and someone from the [core team](https://zenml.io/company#CompanyTeam) will respond.\nOr, if you prefer, [open an issue](https://github.com/zenml-io/zenml/issues/new/choose) on our GitHub repo.\n\n\n# 📜 License\n\nZenML is distributed under the terms of the Apache License Version 2.0. \nA complete version of the license is available in the [LICENSE](LICENSE) file in\nthis repository. Any contribution made to this project will be licensed under\nthe Apache License Version 2.0.\n',
    'author': 'ZenML GmbH',
    'author_email': 'info@zenml.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://zenml.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
