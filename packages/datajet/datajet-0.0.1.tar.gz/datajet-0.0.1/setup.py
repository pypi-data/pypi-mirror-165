# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datajet']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datajet',
    'version': '0.0.1',
    'description': 'A Data Dependency Graph Framework and Executor',
    'long_description': '# DataJet\n\nA Data Dependency Graph Framework and Executor\n\n**Key Features**\n- Lazy: Only Evaluate and return the data you need\n- Declarative: Declare Data Dependencies and transformations explicitly, using plain python\n- Dependency-Free: Just Python. \n\n## Installation\nRequirements:\n- Python >=3.8\n\nTo Get Started, Install DataJet From pypi:\n```bash\npip install datajet\n```\n\n## Usage\nDataJet dependencies are expressed as a `dict`. Each key-value pair in the dict corresponds to a piece of data and specifies how to calculate it:\n\n```python\nfrom datajet import execute\ndatajet_map = {\n    "dollars": [3.99, 10.47, 18.95, 15.16,],\n    "units": [1, 3, 5, 4,],\n    "prices": lambda dollars, units: [d/u for d, u in zip(dollars, units)],\n    "average_price": lambda prices: sum(prices) / len(prices) * 1000 // 10 / 100\n}\nexecute(datajet_map, fields=[\'prices\', \'average_price\'])\n{\'prices\': [3.99, 3.49, 3.79, 3.79], \'average_price\': 3.76}\n```\n\nYou can also override any data declaration at "execute time":\n```python\nexecute(\n        datajet_map, \n        context={"dollars": map(lambda x: x*2, [3.99, 10.47, 18.95, 15.16,])}, \n        fields=[\'average_price\']\n)\n{\'average_price\': 7.52}\n```\n\nKeys can be any hashable. The value corresponding to each key can be a function or an object. The functions can have 0 or more parameters. The parameter names must correspond to other keys in the dict if no explicitly defined inputs to the callable are declared in the map. See [data maps](./data_map.md) for how to explicitly define inputs.\n\nYou can also define multiple ways of calculating a piece of data via defining a list of functions as the value to the key. Again, each function\'s parameters must correspond to other keys in the dict, or else you can define which other keys should be inputs to the function via explicitly defining inputs.\n\nThe benefits of specifying your data like this may not be immediately apparent, but this gets powerful when you create many possible functions:\n\n```python\nfrom datajet import execute \ndepartments =[\n    {"tag": "GR", "value": "GROCERY"}, {"tag": "FZ", "value": "FROZEN"}\n]\n\ncategories = [\n    {"tag": "PB", "value": "Peanut Butter", "department_tag": "GR"},\n    {"tag": "J", "value": "Jelly", "department_tag": "GR",},\n    {"tag": "FZE", "value":"FROZEN ENTREES", "department_tag": "FZ"}\n]\n\nsubcategories = [\n    {"tag": "NPB", "value": "PEANUT BUTTER - NATURAL", "category_tag": "PB"},\n    {"tag": "CPB", "value": "PEANUT BUTTER - CONVENTIONAL", "category_tag": "PB"}\n]\n\ndatajet_map = {\n    "category": lambda category_tag: dict((d[\'tag\'], d[\'value\']) for d in categories).get(category_tag),\n    "category_tag": [\n        lambda category: dict((d[\'value\'], d[\'tag\']) for d in categories).get(category),\n        lambda subcategory: dict((d[\'value\'], d[\'category_tag\']) for d in subcategories).get(subcategory),\n    ],\n    "subcategory": lambda subcategory_tag: dict((d[\'tag\'], d[\'value\']) for d in subcategories).get(subcategory_tag),\n    "department_tag": lambda category: dict((d[\'value\'], d[\'department_tag\']) for d in categories).get(category),\n    "department": lambda department_tag: dict((d[\'tag\'], d[\'value\']) for d in departments).get(department_tag),\n}\nexecute(datajet_map, context={"subcategory_tag": "NPB"}, fields={"department"})\n{\'department\': \'GROCERY\'}\n```\n\nIn the above example, `datajet.execute` knows to traverse the path from `subcategory_tag` -> `subcategory` -> `category` -> `department_tag` -> `department` to find the corresponding `department` to the `subcategory_tag` passed into the context parameter. Datajet will find connections from "the data you have" to "the data you want" in the data dependency tree, execute the given functions, and return the result.\n\nThis framework frees you (the coder) from the need for more global knowledge about how pieces of data are connected when you request data. To define a datapoint you only need local knowledge of it\'s immediate inputs, and datajet finds the fastest path from the data you input to what you need.\n\n\n## Development\n```\ngit clone\nmake install\n```\nThis will start a [poetry shell](https://python-poetry.org/docs/cli/#shell) that has all the dev dependencies installed.\n\n### Development troubleshooting\nIf you see:\n```\nurllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)>\n```\nGo to /Applications/Python3.x and run \'Install Certificates.command\'\n',
    'author': 'Brian Ritz',
    'author_email': 'brianmritz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bmritz/datajet',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
