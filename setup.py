#!/usrbin/env python # -*- coding: us-ascii -*- # vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka bgnori@gmail.com
#
from setuptools import setup

try:
    # add classifiers and download_url syntax to distutils
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
except:
    pass

setup(
  name=python-tonic-library,
  version="0.0.16",
  zip_safe=False,
  description=collection of small codes. "tonic" library for python,
  long_description=This package contains:
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
,
  package_dir={'tonic':'tonic', },
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
  install_requires= ['BeautifulSoup==3.2.0\n', 'ClientForm==0.2.10\n', 'decorator==3.3.2\n', 'distribute==0.6.19\n', 'elementtree==1.2.7-20070827-preview\n', 'feedparser==5.0.1\n', 'nose==1.1.2\n', 'python-memcached==1.47\n', '-e git+git@github.com:bgnori/tonic.git@e6e3a42b3ac291088b1a4bd41ae6d81918f022fa#egg=python_tonic_library-dev\n', 'wsgiref==0.1.2\n']
  author=Noriyuki Hosaka,
  author_email=bgnori@gmail.com,
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

