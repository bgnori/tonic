#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#

#__all__ = ['Null', 'Dict', 'Disk', 'File',
#           'Memcache', 'Hierachy',]
__all__ = ['Null', 'Dict', 'Disk', 'File',
           'Hierachy',]

from tonic.cache.imp_null import Storage as Null
from tonic.cache.imp_dict import Storage as Dict
from tonic.cache.imp_disk import Storage as Disk
from tonic.cache.imp_file import Storage as File
#from tonic.cache.imp_memcache import Storage as Memcache
from tonic.cache.imp_hierachy import Storage as Hierachy



