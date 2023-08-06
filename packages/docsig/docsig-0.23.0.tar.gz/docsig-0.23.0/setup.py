# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docsig']

package_data = \
{'': ['*']}

install_requires = \
['astroid>=2.11.6,<3.0.0', 'object-colors>=2.1.0,<3.0.0', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['docsig = docsig.__main__:main']}

setup_kwargs = {
    'name': 'docsig',
    'version': '0.23.0',
    'description': 'Check signature params for proper documentation',
    'long_description': 'docsig\n======\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: License\n.. image:: https://img.shields.io/pypi/v/docsig\n    :target: https://img.shields.io/pypi/v/docsig\n    :alt: pypi\n.. image:: https://github.com/jshwi/docsig/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/docsig/actions/workflows/ci.yml\n    :alt: CI\n.. image:: https://codecov.io/gh/jshwi/docsig/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/docsig\n    :alt: codecov.io\n.. image:: https://readthedocs.org/projects/docsig/badge/?version=latest\n    :target: https://docsig.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nCheck signature params for proper documentation\n-----------------------------------------------\n\nCurrently supports reStructuredText (Sphinx) and `numpy`\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install docsig\n\nUsage\n-----\n\nCommandline\n***********\n\n.. code-block:: console\n\n    usage: docsig [-h] [-v] [-c] [-D] [-o] [-p] [-n] [-S] [-s STR] [-d LIST] [-t LIST] [path [path ...]]\n\n    Check signature params for proper documentation\n\n    positional arguments:\n      path                     directories or files to check (default: .)\n\n    optional arguments:\n      -h, --help               show this help message and exit\n      -v, --version            show version and exit\n      -c, --check-class        check class docstrings\n      -D, --check-dunders      check dunder methods\n      -o, --check-overridden   check overridden methods\n      -p, --check-protected    check protected functions and classes\n      -n, --no-ansi            disable ansi output\n      -S, --summary            print a summarised report\n      -s STR, --string STR     string to parse instead of files\n      -d LIST, --disable LIST  comma separated list of rules to disable\n      -t LIST, --target LIST   comma separated list of rules to target\n\nOptions can also be configured with the pyproject.toml file\n\nIf you find the output is too verbose then the report can be configured to display a summary\n\n.. code-block:: toml\n\n    [tool.docsig]\n    check-dunders = false\n    check-overridden = false\n    check-protected = false\n    summary = true\n    disable = [\n        "E101",\n        "E102",\n        "E103",\n    ]\n    target = [\n        "E102",\n        "E103",\n        "E104",\n    ]\n\nAPI\n***\n\n.. code-block:: python\n\n    >>> from docsig import docsig\n\n.. code-block:: python\n\n    >>> string = """\n    ... def function(param1, param2, param3) -> None:\n    ...     \'\'\'Summary for passing docstring...\n    ...\n    ...     Explanation for passing docstring...\n    ...\n    ...     :param param1: About param1.\n    ...     :param param2: About param2.\n    ...     :param param3: About param3.\n    ...     \'\'\'\n    ...     """\n    >>> docsig(string=string)\n    0\n\n.. code-block:: python\n\n    >>> string = """\n    ... def function(param1, param2) -> None:\n    ...     \'\'\'Summary for failing docstring...\n    ...\n    ...     Explanation for failing docstring...\n    ...\n    ...     :param param1: About param1.\n    ...     :param param2: About param2.\n    ...     :param param3: About param3.\n    ...     \'\'\'\n    ... """\n    >>> docsig(string=string)\n    2\n    -\n    def function(✓param1, ✓param2, ✖None) -> ✓None:\n        """...\n    <BLANKLINE>\n        :param param1: ✓\n        :param param2: ✓\n        :param param3: ✖\n        """\n    <BLANKLINE>\n    E102: includes parameters that do not exist\n    <BLANKLINE>\n    1\n\nA full list of checks can be found `here <https://docsig.readthedocs.io/en/latest/docsig.html#docsig-messages>`_\n\nClasses\n#######\nChecking a class docstring is not enabled by default, as this check is opinionated, and won\'t suite everyone\n\nThis check will check documentation of `__init__` under the class docstring, and not under `__init__` itself\n\n.. code-block:: python\n\n    >>> string = """\n    ... class Klass:\n    ...     \'\'\'Summary for failing docstring...\n    ...\n    ...     Explanation for failing docstring...\n    ...\n    ...     :param param1: About param1.\n    ...     :param param2: About param2.\n    ...     :param param3: About param3.\n    ...     \'\'\'\n    ...     def __init__(self, param1, param2) -> None:\n    ...         pass\n    ... """\n    >>> docsig(string=string, check_class=True)\n    Klass::11\n    ---------\n    class Klass:\n        """...\n    <BLANKLINE>\n        :param param1: ✓\n        :param param2: ✓\n        :param param3: ✖\n        """\n    <BLANKLINE>\n        def __init__(✓param1, ✓param2, ✖None) -> ✓None:\n    <BLANKLINE>\n    E102: includes parameters that do not exist\n    <BLANKLINE>\n    1\n\nChecking class docstrings can be permanently enabled in the pyproject.toml file\n\n.. code-block:: toml\n\n    [tool.docsig]\n    check-class = true\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': 'jshwi',
    'maintainer_email': 'stephen@jshwisolutions.com',
    'url': 'https://pypi.org/project/docsig/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
