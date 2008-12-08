#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import base

parser = base.Parser(debug=False)
for name, klass in parser.parsers.items():
  print name, klass.regexp_str
