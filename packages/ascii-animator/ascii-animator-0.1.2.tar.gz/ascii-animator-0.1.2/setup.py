#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'ascii-animator',
        version = '0.1.2',
        description = 'A simple ASCII art animator',
        long_description = '# ascii-animator\n[![build](https://github.com/soda480/ascii-animator/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/soda480/ascii-animator/actions/workflows/main.yml)\n[![complexity](https://img.shields.io/badge/complexity-Simple:%205-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)\n[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)\n[![PyPI version](https://badge.fury.io/py/ascii-animator.svg)](https://badge.fury.io/py/ascii-animator)\n[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)\n\nA simple ASCII text animator.\n\nThe `ascii-art-animator` CLI will take as input a GIF image, extract all the frames from it, convert each frame to ASCII art using [ascii-magic](https://pypi.org/project/ascii-magic/), then display each frame to the terminal using [l2term](https://pypi.org/project/l2term/).\n\n### Installation\n```bash\npip install ascii_animator\n```\n\n### Usage\n```\nascii-art-animator --help\nusage: ascii-art-animator [-h] [-s SPEED] [-f FILE] [-d]\n\nAscii Art Animator from GIF\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s SPEED, --speed SPEED\n                        speed of the animation: very_slow, slow, normal, fast (default normal)\n  -f FILE, --file FILE  the path to a gif file\n  -d, --debug           display debug messages to stdout\n```\n\n### Examples\n\n#### ASCII conversion and animation of GIF images\n\nConvert the following [GIF image](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich.gif)\n\n```bash\nascii-art-animator -f docs/images/marcovich.gif\n```\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich-execution.gif)\n\nConvert the following [GIF image](https://github.com/soda480/ascii-animator/blob/main/docs/images/afuera.gif?raw=true)\n\n```bash\nascii-art-animator -f docs/images/afuera.gif -s fast\n```\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/afuera-execution.gif)\n\n#### Game-Of-Life\n\nA Conway [Game-Of-Life](https://github.com/soda480/game-of-life) implementation that uses `ascii_animator` to display the game to the terminal.\n\n### Development\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```bash\ndocker image build \\\n-t \\\nascii-animator:latest .\n```\n\nRun the Docker container:\n```bash\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\nascii-animator:latest \\\nbash\n```\n\nExecute the build:\n```sh\npyb -X\n```\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/ascii-animator',
        project_urls = {},

        scripts = [],
        packages = ['ascii_animator'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {
            'console_scripts': ['ascii-art-animator = ascii_animator.cli:main']
        },
        data_files = [],
        package_data = {},
        install_requires = [
            'l2term~=0.1.6',
            'ascii-magic'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
