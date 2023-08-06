# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yastyleguide',
 'yastyleguide.checkers',
 'yastyleguide.visitors',
 'yastyleguide.visitors.complexity']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3.0,<23.0.0',
 'flake8-annotations-complexity>=0.0.7,<0.0.8',
 'flake8-bandit>=3.0.0,<4.0.0',
 'flake8-black>=0.3.3,<0.4.0',
 'flake8-bugbear>=22.4.25,<23.0.0',
 'flake8-builtins>=1.5.3,<2.0.0',
 'flake8-comprehensions>=3.9.0,<4.0.0',
 'flake8-docstrings>=1.6.0,<2.0.0',
 'flake8-eradicate>=1.2.1,<2.0.0',
 'flake8-expression-complexity>=0.0.11,<0.0.12',
 'flake8-isort>=4.1.1,<5.0.0',
 'flake8-requirements>=1.5.3,<2.0.0',
 'flake8-string-format>=0.3.0,<0.4.0',
 'flake8>=4.0.1,<5.0.0',
 'nitpick>=0.32.0,<0.33.0',
 'pandas-vet>=0.2.3,<0.3.0',
 'pep8-naming>=0.12.1,<0.13.0']

entry_points = \
{'flake8.extension': ['YASG = yastyleguide.plugin:YASGPlugin']}

setup_kwargs = {
    'name': 'yastyleguide',
    'version': '0.1.0',
    'description': 'Yet another styleguide.',
    'long_description': '# yastyleguide\nYet another styleguide\n\n\n## Install\n\n```bash\npoetry add -D yastyleguide\n```\n\n```bash\npip install yastyleguide\n```\n\n## Nitpick styleguide\n\nYou can use base settings for linters with [nitpick](https://github.com/andreoliwa/nitpick):\n```toml\n[tool.nitpick]\nstyle = "https://gitlab.com/ds.team/general/yastyleguide/-/blob/master/styles/nitpick-yastyle.toml"\n```\n<details><summary>Публичный вариант</summary>\n\n```toml\n[tool.nitpick]\nstyle = "https://raw.githubusercontent.com/levkovalenko/yastyleguide/master/styles/nitpick-yastyle.toml"\n```\n</details>\n\n## Running\nIt\'s just plugin **flake8**, so:\n```bash\nflake8 .\n```\n\n## Violations\nOur own codes:\n|Code|Description|\n|----|-----------|\n|YASG101|`Don\'t use any \'for\' loops.`|\n|YASG102|`Don\'t use any \'while\' loops.`|\n|YASG201|`Line is to complex, {0} > {1}. To many ast nodes per line.`|\n|YASG202|`To big median line complexity in module, {0} > {1}.`|\n|YASG203|`To many lines per module, {0} > {1}.`|\n|YASG204|`To many function definitions per module, {0} > {1}.`|\n|YASG205|`To many class definitions per module, {0} > {1}.`|\n\nYou can read about external plugins violations at [/docs/eng/plugin_list.md](docs/eng/plugin_list.md)',
    'author': 'levkovalenko',
    'author_email': 'levozavr@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/levkovalenko/yastyleguide',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
