#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
from distutils.core import setup
import os, os.path


NAME = 'python-tonic-library'
AUTHOR = "Noriyuki Hosaka", "bgnori@gmail.com",
VERSION = open("VERSION").read().strip()
DESCRIPTION = 'collection of small codes. "tonic" library for python'
LONG_DESCRIPTION="""\
This package contains:
 * turbogears:
  * cc: decorators for cache-control.
  * widget: original widgets.
 * lineparser
  * parsing line oriented data.
 * specedit
  * reader/writer for spef file of RPM.
  * It uses elementtree a.k.a xml.etree in python 2.5 or later, for intermediate expression.
"""
HOMEPAGE = "http://www.tonic-water.com/"


try:
    # add classifiers and download_url syntax to distutils
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
except:
    pass

setup(
  name=NAME,
  version=VERSION,
  zip_safe=False,
  description=DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  package_dir={'tonic':'tonic', }, #root
  packages=['tonic',
            'tonic.turbogears',
           ],
  package_data = {},
  py_modules=[
            'tonic.funny',
            'tonic.lineparser',
  ],
  install_requires = [
    "python>=2.4",
    "TurboGears>=1.0.0",
  ],
  author=AUTHOR[0],
  author_email=AUTHOR[1],
  url=HOMEPAGE,
  license="Apache 2.0 Lisence",
  provides=['python-tonic-library'],
  classifiers=[
      "Development Status :: 3 - Alpha",
      "Operating System :: OS Independent",
      "Intended Audience :: Developers",
      "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
      "Framework :: TurboGears",
      "Topic :: Text Processing",
      "Topic :: Software Development",
      "Topic :: System :: Archiving :: Packaging",
      ]
)

