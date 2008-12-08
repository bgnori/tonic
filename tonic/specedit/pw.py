#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import sys
import base

parser = base.Parser()
root = parser.parse(sys.stdin)
assert root is not None
writer = base.Writer()
writer.write(root, sys.stdout)


