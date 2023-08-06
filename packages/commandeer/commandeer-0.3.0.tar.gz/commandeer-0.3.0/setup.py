# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commandeer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'commandeer',
    'version': '0.3.0',
    'description': 'A command-line parser library',
    'long_description': "Commandeer is a command-line generator library that you can use to add a nice command line interface to your python programs.\n\nIt will take care of parsing all command line options as well as calling the right command functions in your script. And it will generate a nice-looking help for the program and for each of the commands.\n\nWe've written Commandeer in such a way that it should work just like you expect it to. There are only two things you need to do:\n * name the functions you want to expose on the command line to end in ``_command``.\n * Add the following code snippet to the end of your command line module::\n\n       import commandeer\n       if __name__ == '__main__':\n           commandeer.cli()\n\nYou should try it out!\n\nFor more information, consult the documentation on\n  https://gitlab.com/jspielmann/commandeer/\n  \n  \nLicense information\n-------------------\n\nCopyright (C) 2012, 2021 Johannes Spielmann\n\nCommandeer is licensed under the terms of the GNU General Public Licenses as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\nFor a full description of the license, please see the file\n\n    LICENSE\n",
    'author': 'Johannes Spielmann',
    'author_email': 'j@spielmannsolutions.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/jspielmann/commandeer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
