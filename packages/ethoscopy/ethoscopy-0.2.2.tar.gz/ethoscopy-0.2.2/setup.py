# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ethoscopy', 'ethoscopy.misc']

package_data = \
{'': ['*']}

install_requires = \
['hmmlearn>=0.2.7,<0.3.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.7.0,<6.0.0',
 'scipy>=1.8.0,<2.0.0',
 'tabulate>=0.8.10,<0.9.0']

setup_kwargs = {
    'name': 'ethoscopy',
    'version': '0.2.2',
    'description': 'A python based toolkit to download and anlyse data from the Ethoscope hardware system.',
    'long_description': "**ethoscopy**\n\nA data-analysis toolbox utilising the python language for use with data collected from 'Ethoscopes', a Drosophila video monitoring system.\n\nFor more information on the ethoscope system: https://www.notion.so/The-ethoscope-60952be38787404095aa99be37c42a27\n\nEthoscopy is made to work alongside this system, working as a post experiment analysis toolkit. \n\nEthoscopy provides the tools to download epxerimental data from a remote ftp servers as setup in ethoscope tutorial above. Downloaded data can be curated during the pipeline in a range of ways, all fromatted using the pandas data structure.\n\nFurther the ethoscopy package provides behavpy a subclassed version of pandas that combines metadata with the data for easy manipulation. Behavpy can be used independantly of the Ethoscope system data if following the same structure.\n\nWithin Behavpy is a wrapped version of the python package hmmlearn, a tool for creating hidden markov models. With the update the user can easy train new HMMs from their data.\n\n**To Come**\nPlotting functions to complement the addtioanal hmmlearn update\n\n",
    'author': 'Blackhurst Laurence',
    'author_email': 'l.blackhurst19@imperial.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
