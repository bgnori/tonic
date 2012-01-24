#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka bgnori@gmail.com
#

from setuptools import setup

NAME = 'python-tonic-library'
AUTHOR = "Noriyuki Hosaka", "bgnori@gmail.com",
VERSION = open("VERSION").read().strip()
DESCRIPTION = 'collection of small codes. "tonic" library for python'
LONG_DESCRIPTION = """\
This package contains:
 * lineparser
  * parsing line oriented data.

 * cache
  * interface/implementation for cache something. 
  * supports
   * using dict
   * using disk
   * using file (key for get/set must be valid path)
   * using memcache
  * multithread is currently NOT supported

 * math related
  * combination

 * funny
  * __dict__/__setattr__ joke

 * other
  * feedhelper => will move out as app
  * 


"""
  


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
           ],
  package_data = {},
  py_modules=[
            'tonic.funny',
            'tonic.lineparser',
            'tonic.combination',
            'tonic.visitbus',
            'tonic.bitsarray',
  ],
  install_requires=open('freeze.txt').readlines(),
  author=AUTHOR[0],
  author_email=AUTHOR[1],
  url="http://github.com/bgnori/tonic",
  license="Apache 2.0 Lisence",
  provides=['tonic'],
  classifiers=[
      "Development Status :: 3 - Alpha",
      "Operating System :: OS Independent",
      "Intended Audience :: Developers",
      "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
      "Topic :: Text Processing",
      "Topic :: Software Development",
      "Topic :: System :: Archiving :: Packaging",
      ]
)

