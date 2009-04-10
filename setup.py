#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka bgnori@gmail.com
#

from distutils.core import setup
import os

from tonic.moduleid import *

NAME = 'python-tonic-library'
AUTHOR = "Noriyuki Hosaka", "bgnori@gmail.com",
VERSION = open("VERSION").read().strip()
DESCRIPTION = 'collection of small codes. "tonic" library for python'
LONG_DESCRIPTION = 'build id is "%s". \n'%(register(globals()),)+ \
  """\
This package contains:
 * turbogears:
  * cc: decorators for cache-control.
  * widget: original widgets.

 * lineparser
  * parsing line oriented data.

 * moduleid 
  * calc moduleid based sha1 on content of __file__

 * specedit
  * reader/writer for spef file of RPM.
  * It uses elementtree a.k.a xml.etree in python 2.5 or later, for intermediate expression.
  * It uses feature in originally packaged elementtree for testing.

 * cache
  * interface/implementation for cache something. 
  * supports
   * using dict
   * using disk
   * using file (key for get/set must be valid path)
   * using memcache
  * multithread is currently NOT supported

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
            'tonic.cache',
            'tonic.depot',
            'tonic.feedhelper',
            'tonic.markups',
            'tonic.specedit',
            'tonic.tg',
           ],
  package_data = {},
  py_modules=[
            'tonic.funny',
            'tonic.lineparser',
            'tonic.combination',
            'tonic.visitbus',
            'tonic.bitsarray',
            'tonic.moduleid',
  ],
  install_requires = [
    "python>=2.4",
    "TurboGears>=1.0.0",
    "python-elementtree>=1.3.a3", 
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
      "Framework :: TurboGears",
      "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
      "Topic :: Text Processing",
      "Topic :: Software Development",
      "Topic :: System :: Archiving :: Packaging",
      "Topic :: Software Development :: Build Tools",
      ]
)

