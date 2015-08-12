#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

install_requires = []
PY_VER = sys.version_info

if PY_VER >= (3, 4):
    pass
elif PY_VER >= (3, 3):
    install_requires.append('asyncio')
else:
    raise RuntimeError("aioavast doesn't suppport Python earlier than 3.3")


def read(*parts):
    with open(os.path.join(*parts), 'rt') as f:
        return f.read().strip()


setup(name='aioavast',
      version='1.0.0',
      description=('Asyncio library for Avast antivirus'),
      long_description=read('README.rst'),
      url='http://github.com/earada/aioavast',
      author='Eduardo Arada',
      author_email='eduardo.arada@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Security',
          ],
      platforms=['POSIX'],
      download_url='https://pypi.python.org/pypi/aioavast',
      packages=find_packages(),
      install_requires=install_requires,
      include_package_data = True)
