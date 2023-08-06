# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mystbin', 'mystbin.types']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['aiohttp>=3.7.4,<4.0.0']

extras_require = \
{'docs': ['sphinx>=4.0.0,<5.0.0', 'sphinxcontrib-trio', 'furo'],
 'requests': ['requests>=2.24.0,<3.0.0']}

entry_points = \
{'console_scripts': ['version = mystbin.__main__:show_version']}

setup_kwargs = {
    'name': 'mystbin-py',
    'version': '5.0.1',
    'description': 'A small simple wrapper around the mystb.in API.',
    'long_description': '<div align="center">\n    <h1>Mystbin.py!</h1>\n    <a href=\'https://mystbinpy.readthedocs.io/en/latest/?badge=latest\'>\n        <img src=\'https://readthedocs.org/projects/mystbinpy/badge/?version=latest\' alt=\'Documentation Status\' />\n    </a>\n    <a href=\'https://github.com/PythonistaGuild/mystbin.py/workflows/Code%20Linting\'>\n        <img src=\'https://github.com/PythonistaGuild/mystbin.py/workflows/Code%20Linting/badge.svg?branch=main\' alt=\'Linting status\' />\n    </a>\n    <a href=\'https://github.com/PythonistaGuild/mystbin.py/workflows/Build\'>\n        <img src=\'https://github.com/PythonistaGuild/mystbin.py/workflows/Build/badge.svg\' alt=\'Build status\' />\n    </a>\n</div>\n<br>\n\nA small simple wrapper around the [Mystb.in](https://mystb.in/) API. API docs can be found [here](https://api.mystb.in/docs).\n\nDocumentation for this wrapper can be found [here](https://mystbinpy.readthedocs.io/en/stable/).\nIf you want the docs for the `main` branch, those can be found [here](https://mystbinpy.readthedocs.io/en/latest/).\n\n----------\n### Features\n\n- [x] - Creating pastes.\n- [ ] - Editing pastes.\n    - Pending design work.\n- [x] - Deleting pastes.\n- [x] - Getting pastes.\n- [ ] - User endpoints.\n- [ ] - Sync client.\n  - This one will take some time as I have no motivation to do it, but PRs are welcome if others want to do it.\n\n### Installation\nThis project will be on [PyPI](https://pypi.org/project/mystbin.py/) as a stable release, you can always find that there.\n\nInstalling via `pip`:\n```shell\npython -m pip install -U mystbin.py\n```\n\nInstalling from source:\n```shell\npython -m pip install git+https://github.com/PythonistaGuild/mystbin.py.git\n```\n\n### Usage examples\nSince the project is considered multi-sync, it will work in a sync/async environment, see the optional dependency of `requests` below.\n\n```py\n# async example - it will default to async\nimport mystbin\n\nmystbin_client = mystbin.Client()\n\npaste = await client.create_paste(filename="Hello.txt", content="Hello there!", syntax="txt")\nstr(paste)\n>>> \'https://mystb.in/<your generated ID>\'\n\nget_paste = await mystbin_client.get_paste("<your generated ID>")\nget_paste.files[0].content\n>>> "Hello there!"\n\nget_paste.created_at\n>>> datetime.datetime(2020, 10, 6, 10, 53, 57, 556741)\n```\n\nOr if you want to create a paste with multiple files...\n```py\nimport mystbin\n\nfile = mystbin.File(filename="File1.txt", content="Hello there!", syntax="txt")\nfile2 = mystbin.File(filename="test.py", content="print(\'hello!\')", syntax="py")\n\npaste = await client.create_multifile_paste(files=[file, file2])\n\nfor file in paste.files:\n    print(file.content)\n\n>>> "Hello there!"\n>>> "print(\'hello!\')"\n```\n\nIf you have any question please feel free to join the Pythonista Discord server:\n<div align="left">\n    <a href="https://discord.gg/RAKc3HF">\n        <img src="https://discordapp.com/api/guilds/490948346773635102/widget.png?style=banner2" alt="Discord Server"/>\n    </a>\n</div>\n',
    'author': 'AbstractUmbra',
    'author_email': 'Umbra@AbstractUmbra.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PythonistaGuild/mystbin.py',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
