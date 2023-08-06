# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makros', 'makros.macros', 'makros.registration']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.4.4,<13.0.0']

entry_points = \
{'console_scripts': ['makros = makros.cli:cli']}

setup_kwargs = {
    'name': 'makros',
    'version': '1.0.0',
    'description': 'Modify and extend the Python language with (relative) ease',
    'long_description': '<div align="center">\n\n# Makros\n\nExtend the Python language with (relative) ese\n\n</div>\n\nThis program converts custom python files with a custom syntax to regular python files. The overall goals of this project are:\n\n1.  To include some of the features that I feel are missing from the python programming language\n2.  Provide a method for others to use this functionality without needing to contribute to this repo\n\n## Installation\n\n```bash\npip install makros\n```\n\n## Usage\n\nTo use this simply create a file with the `.mpy` extension, like the following:\n\n```python\nmacro import namespace\n\nnamespace greet:\n    name = "World"\n\n    export def set_name(new_name):\n        name = new_name\n\n    export def say_hello():\n        print("Hello, " + name)\n\ngreet.say_hello()\ngreet.set_name("trickypr")\ngreet.say_hello()\n```\n\nThen just run it with makros:\n\n```bash\nmakros my_file.mpy\n```\n\nFor more info, please [read our docs](https://makros.trickypr.com/docs/).\n',
    'author': 'trickypr',
    'author_email': 'trickypr@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
