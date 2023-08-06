# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli_ui', 'cli_ui.tests']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.1,<0.5.0', 'tabulate>=0.8.3,<0.9.0', 'unidecode>=1.0.23,<2.0.0']

setup_kwargs = {
    'name': 'cli-ui',
    'version': '0.17.2',
    'description': 'Build Nice User Interfaces In The Terminal',
    'long_description': '.. image:: https://img.shields.io/pypi/pyversions/cli-ui.svg\n  :target: https://pypi.org/project/cli-ui\n\n.. image:: https://img.shields.io/pypi/v/cli-ui.svg\n  :target: https://pypi.org/project/cli-ui/\n\n.. image:: https://img.shields.io/github/license/your-tools/python-cli-ui.svg\n  :target: https://github.com/your-tools/python-cli-ui/blob/main/LICENSE\n\n.. image:: https://img.shields.io/badge/deps%20scanning-pyup.io-green\n  :target: https://github.com/your-tools/python-cli-ui/actions\n\npython-cli-ui\n=============\n\nTools for nice user interfaces in the terminal.\n\nNote\n----\n\nThis project was originally hosted on the `TankerHQ\n<https://github.com/TankerHQ>`_ organization, which was my employer from 2016\nto 2021. They kindly agreed to give back ownership of this project to\nme. Thanks!\n\nDocumentation\n-------------\n\n\nSee `python-cli-ui documentation <https://your-tools.github.io/python-cli-ui>`_.\n\nDemo\n----\n\n\nWatch the `asciinema recording <https://asciinema.org/a/112368>`_.\n\n\nUsage\n-----\n\n.. code-block:: console\n\n    $ pip install cli-ui\n\nExample:\n\n.. code-block:: python\n\n    import cli_ui\n\n    # coloring:\n    cli_ui.info(\n      "This is",\n      cli_ui.red, "red", cli_ui.reset,\n      "and this is",\n      cli_ui.bold, "bold"\n    )\n\n    # enumerating:\n    list_of_things = ["foo", "bar", "baz"]\n    for i, thing in enumerate(list_of_things):\n        cli_ui.info_count(i, len(list_of_things), thing)\n\n    # progress indication:\n    cli_ui.info_progress("Done",  5, 20)\n    cli_ui.info_progress("Done", 10, 20)\n    cli_ui.info_progress("Done", 20, 20)\n\n    # reading user input:\n    with_sugar = cli_ui.ask_yes_no("With sugar?", default=False)\n\n    fruits = ["apple", "orange", "banana"]\n    selected_fruit = cli_ui.ask_choice("Choose a fruit", choices=fruits)\n\n    #  ... and more!\n\nContributing\n------------\n\nWe use `optimistic merging <https://dmerej.info/blog/post/optimistic-merging/>`_ so you don\'t have to worry too much about formatting the code, pleasing the linters or making sure all the test pass.\n\nThat being said, if you want, you can install `just <https://just.systems/man/en/>`_ and use it to check your changes automatically. Just run ``just`` to see available tasks.\n',
    'author': 'Dimitri Merejkowsky',
    'author_email': 'dimitri@dmerej.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~your-tools/python-cli-ui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
