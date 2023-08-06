# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['axe_core_python']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'axe-core-python',
    'version': '0.1.0',
    'description': 'Automated web accessibility testing using axe-core engine.',
    'long_description': '# axe-core-python\n\n![PyPI](https://img.shields.io/pypi/v/axe-core-python) \n![PyPI - License](https://img.shields.io/pypi/l/axe-core-python) \n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/axe-core-python)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/axe-core-python) \n\n\nAutomated web accessibility testing using [axe-core](https://github.com/dequelabs/axe-core) engine.\n\n## Documentation\n\n- [Full documentation](https://ruslan-rv-ua.github.io/axe-core-python/).\n\n## Requirements\n\n- Python >= 3.10\n- [selenium](https://www.selenium.dev) >= 4.4.0 \nor [playwright](https://github.com/microsoft/playwright-python) >= 1.25.0\n\n## Installation\n\n```console\npip install -U axe-core-python\n```\n\n## Usage\n\n```python\nfrom playwright.sync_api import sync_playwright\nfrom axe_core_python.sync_playwright import Axe\n\naxe = Axe()\n\nwith sync_playwright() as playwright:\n    browser = playwright.chromium.launch()\n    page = browser.new_page()\n    page.goto("https://www.google.com")\n    result = axe.run(page)\n    browser.close()\n\nviolations = result[\'violations\']\nprint(f"{len(violations)} violations found.")\n```\n\nFor more examples see [documentation](https://ruslan-rv-ua.github.io/axe-core-python/).',
    'author': 'Ruslan Iskov',
    'author_email': 'ruslan.rv.ua@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ruslan-rv-ua/axe-core-python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
