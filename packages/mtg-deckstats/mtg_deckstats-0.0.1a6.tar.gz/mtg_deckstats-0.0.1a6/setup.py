# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mtg_deckstats']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'more-itertools>=8.13.0,<9.0.0',
 'mtg-parser>=0.0.1-alpha.26,<0.0.2',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'mtg-deckstats',
    'version': '0.0.1a6',
    'description': 'Magic: the Gathering deckstats',
    'long_description': "# mtg-deckstats\n\n![PyPI](https://img.shields.io/pypi/v/mtg-deckstats)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mtg-deckstats)\n![GitHub](https://img.shields.io/github/license/lheyberger/mtg-deckstats)\n\n\n## How to install\n\n\tpip install mtg-deckstats\n\n\n## Quick Start\n\nGenerate a deckstats report using the following steps:\n\n\timport mtg_deckstats\n\t\n\treport = mtg_deckstats.compute('<decklist url>')\n\tprint(report)\n\n\nTo speed things up, you can also compute reports with a pre-generated cache using the following steps:\n\n\timport mtg_deckstats\n\n\tcache = mtg_deckstats.pre_cache()\n\n\treport_1 = mtg_deckstats.compute('<decklist url 1>', data=cache)\n\tprint(report_1)\n\n\treport_2 = mtg_deckstats.compute('<decklist url 2>', data=cache)\n\tprint(report_2)\n\n\n## Supported deckbuilding websites\n\nInternally `mtg_deckstats` relies on `mtg_parser` and thus, supports the following deckbuilding websites:\n* aetherhub.com\n* archidekt.com\n* deckstats.net\n* moxfield.com\n* mtggoldfish.com\n* scryfall.com\n* tappedout.net\n* tcgplayer.com\n",
    'author': 'Ludovic Heyberger',
    'author_email': '940408+lheyberger@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lheyberger/mtg-deckstats',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
