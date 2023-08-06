# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.comm',
 'src.core',
 'src.dataset',
 'src.storage',
 'src.storage.classes',
 'src.tests',
 'src.user',
 'src.user.database',
 'src.user.license',
 'stack_api']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.60,<2.0.0',
 'fastapi>=0.80.0,<0.81.0',
 'google-cloud-datastore>=2.8.1,<3.0.0',
 'google-cloud-storage>=2.5.0,<3.0.0',
 'maskpass>=0.3.6,<0.4.0',
 'pymongo>=4.2.0,<5.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['stackcli = stack_api.api_cli:app']}

setup_kwargs = {
    'name': 'stackcli',
    'version': '0.1.2',
    'description': '',
    'long_description': "# Stack\n\n### Install Stack\n\n1. Open your favorite terminal: `Terminal`\n2. Install stackcli: `pip install stackcli` (ideally in a virtualenv)\n\n### Build a test dataset\n\n1. Make a directory: `mkdir test_dataset`\n2. Go to the directory: `cd test_dataset`\n3. Download an image of Einstein: `curl -o einstein.jpg https://upload.wikimedia.org/wikipedia/en/8/86/Einstein_tongue.jpg`\n\n\n### Try Stack's Command Line Tool (CLI)\n\n1. Init stack in the current directory: ```stackcli init . ``` (note the dot at the end)\n2. Add a file to track: `stackcli add einstein.jpg`\n3. Commit your changes: `stackcli commit`\n4. Check status: `stackcli status`\n5. See history of changes: `stackcli history`\n6. Remove the file: `stackcli remove einstein.jpg`\n7. Revert your changes: `stackcli revert 1`\n8. You should see Einstein in your directory again!\n\n\n# Stack Dev (Ignore if you are just a user)\n\n### Features to implement\n\n### Publish to TestPy\n\nhttps://typer.tiangolo.com/tutorial/package/\n\n1. Install package: `poetry install'\n2. Try CLI: find it first `which stackcli`\n3. Create a wheel package: `poetry build'\n4. Test wheel: `pip install --user dist'\n5. Try the wheel: `stackcli`\n6. Publish it to TestPy: `poetry publish --build'\n7. Install from TestPyPI:\n  1. `pip uninstall stack-cli`\n  1. `pip install -i https://test.pypi.org/simple/ stack-cli`\n",
    'author': 'Toni Rosinol',
    'author_email': 'arosinol@getstack.ai',
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
