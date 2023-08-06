# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['astral_projection']
install_requires = \
['colorful>=0.5.4,<0.6.0', 'dont>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'astral-projection',
    'version': '0.1.1',
    'description': 'Run code inside a context manager on a remote machine',
    'long_description': '# astral-projection\n\nLike it\'s real-world counterpart (if you can call it that), this package allows\nyour code to have out-of-body experiences. Its effectiveness is also disputed\nby experts.\n\n\n## Usage:\n\n```python\nimport sys\nimport os\nfrom astral_projection import host\n\nx = 23\n\nwith host("l3vi.de"):\n    os.system("hostname")\n    print("hello!", x)\n    for i in range(10):\n        print("hi", i, file=sys.stderr)\n    x += 1\n\nprint("x is now", x)\n```\n',
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/L3viathan/astral-projection',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
