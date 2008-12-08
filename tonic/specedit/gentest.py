#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
'''
What to verify:
1) written output must be parsable.
2) written output must be equal to input beside some exception.
'''

code = """\
#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
# This test file is auto generated. 
#  don't commit.
#  don't edit.
#
import StringIO
import unittest
from tonic import specedit
class SanityTest(unittest.TestCase):
  def setUp(self):
    self.source = file('%s')
    self.parser = specedit.Parser()
    self.writer = specedit.Writer()
    self.root = self.parser.parse(self.source)
    self.dest = StringIO.StringIO()
    self.work = StringIO.StringIO()

  def tearDown(self):
    self.source.close()
    self.dest.close()
    self.work.close()

  def test_write(self):
    self.writer.write(self.root, self.dest)

  def test_write_and_parse(self):
    self.writer.write(self.root, self.work)
    self.work.seek(0)
    root = self.parser.parse(self.work)
    self.writer.write(root, self.dest)
    self.assertEqual(self.dest.getvalue(), self.work.getvalue())
"""

import os.path as path
import glob

for g in glob.glob('./tonic/specedit/testdata/*.spec'):
  spec = path.abspath(g)
  test = spec[:-5] + '_test.py'
  print 'writing', test
  f = file(test, 'w+a')
  try:
    f.write(code%spec)
  finally:
    f.close()


