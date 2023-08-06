# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_firewall_models',
 'nautobot_firewall_models.api',
 'nautobot_firewall_models.management',
 'nautobot_firewall_models.management.commands',
 'nautobot_firewall_models.migrations',
 'nautobot_firewall_models.models',
 'nautobot_firewall_models.templatetags',
 'nautobot_firewall_models.tests',
 'nautobot_firewall_models.utils',
 'nautobot_firewall_models.views']

package_data = \
{'': ['*'],
 'nautobot_firewall_models': ['templates/nautobot_firewall_models/*',
                              'templates/nautobot_firewall_models/inc/*']}

install_requires = \
['capirca>=2.0.6,<3.0.0', 'netutils>=1.0.0,<2.0.0']

extras_require = \
{':extra == "nautobot"': ['nautobot>=1.3.0,<2.0.0']}

setup_kwargs = {
    'name': 'nautobot-firewall-models',
    'version': '1.0.0',
    'description': 'Nautobot plugin to model firewall objects.',
    'long_description': '# Nautobot Firewall Models Plugin\n\nA plugin for [Nautobot](https://github.com/nautobot/nautobot) that is meant to model layer 4 firewall policies and/or extended access control lists. \n\nFuture development will include the ability to onboard an existing access list from a device and the ability to generate device configuration.\n\n## Installation\n\nThe plugin is available as a Python package in PyPI and can be installed with `pip`:\n\n```shell\npip install nautobot-firewall-models\n```\n\n> The plugin is compatible with Nautobot 1.4.0 and higher\n\nTo ensure Nautobot Firewall Models Plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-firewall-models` package:\n\n```no-highlight\n# echo nautobot-firewall-models >> local_requirements.txt\n```\n\nOnce installed, the plugin needs to be enabled in your `nautobot_config.py`\n\n```python\n# In your nautobot_config.py\nPLUGINS = ["nautobot_firewall_models"]\n```\n\n## Optional Settings\n\nModels provided by this plugin have a `status` attribute and the default `status` is set to use `active`. This corresponds to the pre-built Nautobot `Active` Status object.\n\nUse the `default_status` plugin configuration setting to change the default value for the `status` attribute.\n\n```python\nPLUGINS_CONFIG = {\n    "nautobot_firewall_models": {\n        "default_status": "active"\n        "allowed_status": ["active"], # default shown, `[]` allows all\n        "capirca_remark_pass": True,\n        "capirca_os_map": {\n            "cisco_ios": "cisco",\n            "arista_eos": "arista",\n        },\n        # "custom_capirca": "my.custom.func", # provides ability to overide capirca logic\n    }\n}\n```\n\nThe value assigned to `default_status` must match the slug of an existing Nautobot Status object. That Status object must have all of the Firewall Models listed in the Content Type associations. See examples below on selecting the Content Type(s) when creating/editing a Status object and the pre-built `Active` Status with firewall content types added.\n\n![Custom Status](https://raw.githubusercontent.com/nautobot/nautobot-plugin-firewall-models/develop/docs/images/custom-status.png "Custom Status")\n![Existing Status](https://raw.githubusercontent.com/nautobot/nautobot-plugin-firewall-models/develop/docs/images/existing-status.png "Existing Status")\n\n## Screenshots\n\n![Navigation Menu](https://raw.githubusercontent.com/nautobot/nautobot-plugin-firewall-models/develop/docs/images/navmenu.png "Navigation Menu")\n![Policy View](https://raw.githubusercontent.com/nautobot/nautobot-plugin-firewall-models/develop/docs/images/policy.png "Policy View")\n\n## Documentation\n\nDocumentation is hosted on ReadTheDocs at [Nautobot Firewall Models Plugin](https://nautobot-plugin-firewall-models.readthedocs.io/).\n\n## Contributing\n\nPull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.\n\nThe project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.\n\nThe project is following Network to Code software development guideline and is leveraging:\n\n- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.\n- Django unit test to ensure the plugin is working properly.\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).\nSign up [here](http://slack.networktocode.com/)\n',
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nautobot/nautobot-plugin-firewall-models',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
