# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymafia', 'pymafia.datatypes', 'pymafia.iotms']

package_data = \
{'': ['*']}

install_requires = \
['pyjnius>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'pymafia',
    'version': '0.0.3',
    'description': "A Python module and bridge for reflecting KoLmafia's Java environment.",
    'long_description': '# pymafia\n\nA Python module and bridge for reflecting KoLmafia\'s Java environment.\n\n## Overview\n\nThe aim of the `pymafia` module is to provide an easy-to-use environment for scripting [Kingdom of Loathing](https://www.kingdomofloathing.com/) in Python. It achieves this by reflecting and wrapping the community-developed [KoLmafia](https://github.com/kolmafia/kolmafia) desktop tool. While [other languages](https://loathing-associates-scripting-society.github.io/KoL-Scripting-Resources/) for scripting KoL exist, they are arguably less approachable to non-developers than Python (although the efforts of [LASS](https://github.com/Loathing-Associates-Scripting-Society) have made this less so).\n\n## Installation\n\n```\npip install pymafia\n```\nThe `pymafia` module uses [PyJNIus](https://github.com/kivy/pyjnius) to access Java classes, so make sure a Java Development Kit (JDK) is installed on your operating system. On windows, make sure `JAVA_HOME` points to your java installation so PyJNIus can locate the `jvm.dll` file to start java. For more information see https://pyjnius.readthedocs.io/en/stable/installation.html.\n\n## Quickstart\n\n```python\n>>> from pymafia import *\n\n>>> login("devster6")\n>>> ash.my_name()\n"devster6"\n\n>>> Effect("Synthesis: Greed").quality\n<EffectQuality.GOOD: 0>\n\n>>> ash.display_amount(Item("big rock"))\n6540\n\n>>> ash.appearance_rates(Location("Barf Mountain"))\n{Monster(\'none\'): 0.0,\n Monster(\'angry tourist\'): 33.333333333333336,\n Monster(\'horrible tourist family\'): 33.333333333333336,\n Monster(\'garbage tourist\'): 33.333333333333336}\n\n>>> get_property("sourceTerminalEducate1")\n\'digitize.edu\'\n\n>>> get_property("_sourceTerminalDigitizeMonster", Monster)\nMonster(\'Knob Goblin Embezzler\')\n\n>>> boxing_daycare.have()\nTrue\n\n>>> witchess.fights_left()\n5\n```\n',
    'author': 'MrFizzyBubbs',
    'author_email': 'MrFizzyBubbs@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrFizzyBubbs/pymafia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
