# © Copyright 2022 CERN. This software is distributed under the terms of
# the GNU General Public Licence version 3 (GPL Version 3), copied verbatim
# in the file 'LICENCE.txt'. In applying this licence, CERN does not waive
# the privileges and immunities granted to it by virtue of its status as an
# Intergovernmental Organization or submit itself to any jurisdiction.

"""
NOTED PyPI repository: https://pypi.org/project/noted-dev
Build and package info:
https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_namespace_packages
from setuptools.command.build_py import build_py
import subprocess
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding = 'utf-8')

class Build(build_py):
    """Specialized Python source builder."""

    def run(self):
        """Run command."""
        subprocess.call('./src/noted/scripts/setup.sh setup', shell = True)
        build_py.run(self)

def get_requirements(file):
    # pylint: disable = invalid-name
    with open(file) as f:
        lines = [line.strip() for line in f.readlines()]
    return [module for module in lines if module and not module.startswith('#')]

setup(
    name = 'noted-dev', # pip install noted-dev
    version = '1.1.34',
    description = 'NOTED: a framework to optimise network traffic via the analysis of data from File Transfer Services',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://gitlab.cern.ch/mmisamor/noted',
    author = 'Carmen Misa Moreira, Edoardo Martelli (CERN IT-CS-NE)',
    author_email = 'carmen.misa.moreira@cern.ch',
    license = 'GPLv3 (GNU General Public License)',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: System :: Networking :: Monitoring',
    ],
    keywords = 'networking, monitoring, transfers, dynamic circuit, load balance, fts, sense-o',
    package_dir = {'': 'src'},
    packages = find_namespace_packages(where = 'src', include = ['noted', 'noted.config', 'noted.documentation', 'noted.html',  'noted.modules', 'noted.params', 'noted.sense-o']),
    include_package_data = True,
    python_requires = '>=3',
    setup_requires = ['wheel'],
    entry_points = {
        'console_scripts': [
            'noted = noted.main:main',
        ],
    },
    install_requires = get_requirements('requirements.txt'), # pip freeze > requirements.txt
    project_urls = {'Source': 'https://gitlab.cern.ch/mmisamor/noted'},
    scripts=[
        'src/noted/scripts/setup.sh',
    ],
    cmdclass = {'build_py': Build},
)
