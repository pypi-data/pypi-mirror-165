# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resotoclient']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0',
 'cryptography>=36.0.2',
 'jsons>=1.6.1,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.27.1,<3.0.0']

extras_require = \
{'extras': ['pandas>=1.4.2,<2.0.0', 'graphviz>=0.20,<0.21']}

setup_kwargs = {
    'name': 'resotoclient',
    'version': '0.1.14',
    'description': 'Resoto Python client library',
    'long_description': '# resotoclient-python\nPython client for Resoto\n\n## Installation\n```bash\npip install resotoclient\n```\n\nFor GraphVis and Pandas support:\n\n```bash\npip install resotoclient[extras]\n```\n\n## Usage\n```python\nfrom resotoclient import ResotoClient\n\nclient = ResotoClient(url="https://localhost:8900", psk="changeme")\ninstances_csv = client.cli_execute("search is(instance) | tail 5 | list --csv")\n\nfor instance in instances_csv:\n    print(instance)\n```\n\n### Pandas Dataframes\n```python\ndf = client.dataframe("is(instance)")\n```\n\n### GraphViz Digraph\n```python\ngraph = client.graphviz("is(graph_root) -->")\n```\n\n## Test\nThe tests expect a ResotoCore on localhost with the default PSK `changeme`.\nYou can start it locally via:\n\n```bash\n$> resotocore --graphdb-database resotoclient_test --psk changeme\n```\n\nA local test environment is required. See the [contribution guide](https://resoto.com/docs/contributing/components) for instructions.\nWhen the virtual environment is available, use those commands to set up the project and run the tests:\n\n```bash\n$> pip install --upgrade pip poetry nox nox-poetry\n$> nox\n```\n\nFor more examples see the examples directory.\n\n## Publish\n- bump the version number in pyproject.toml\n- `poetry build`\n- `poetry publish`\n',
    'author': 'Some Engineering Inc.',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/someengineering/resotoclient-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
