#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#

import tempfile
import unittest
import nose

import tonic.depot.lines

class LinesTest(unittest.TestCase):
  def setUp(self):
    self.temp = tempfile.NamedTemporaryFile()
    self.lines_proxy = tonic.depot.lines.Proxy('./tonic/depot/lines_test.txt')

  def tearDown(self):
    pass

  def creation_test(self):
    self.assertNotEqual(self.lines_proxy, None)
    self.assert_(isinstance(self.lines_proxy, tonic.depot.lines.CRLFProxy))

  def secion_test(self):
    self.assert_('logging' in self.lines_proxy)
    self.assert_(hasattr(self.lines_proxy, 'logging'))
    self.assert_(hasattr(self.lines_proxy, 'CommandDebugger'))
    self.assert_(hasattr(self.lines_proxy, 'a'))
    self.assert_(hasattr(self.lines_proxy, 'b'))
    self.assert_(hasattr(self.lines_proxy, 'c'))

  def option_test(self):
    logging = self.lines_proxy.logging
    self.assert_(hasattr(logging, 'level'))
    self.assert_(hasattr(logging, 'format'))
    self.assert_(hasattr(logging, 'filename'))
    self.assert_(hasattr(logging, 'filemode'))

  def value_read_test(self):
    logging = self.lines_proxy.logging
    self.assertEqual(logging.level, '10')
    #self.assertEqual(logging.format, r"'%(asctime)s %(levelname)s %(message)s'")
    self.assertEqual(logging.filename, './wxPyGammon.log')
    self.assertEqual(logging.filemode, 'w')

  def value_write_test(self):
    c = self.lines_proxy.c
    self.assertEqual(c.port, '4321')
    c.port = '54321'
    #self.assertEqual(c.port, '54321')

    #tonic.depot.lines.write(self.lines_proxy, self.temp.name)

    #p = tonic.depot.cfg.CFGProxy([self.temp.name])
    #self.assertEqual(p.c.port, '54321')

  def repr_test(self):
    self.assertEqual(repr(self.lines_proxy), (
        r"""<lines.Proxy for [] of  {'a': {'username': 'bgnori', 'host': 'fibs.com', """
        r"""'password': 'NULL', 'protocol': 'fibs', 'name': 'bgnori@fibs.com:4321', """
        r"""'client_name': 'wxPyGammon-alpha-0.1', 'clip_version': '1008', 'port': """
        r"""'4321'}, 'c': {'username': 'wxpygammon', 'host': 'localhost', 'password': """
        r"""'boo', 'protocol': 'fibs', 'name': 'wxpygammon@localhost:4321', 'client_name': """
        r"""'wxPyGammon-alpha-0.1', 'clip_version': '1008', 'port': '4321'}, 'b': """
        r"""{'username': 'wxpygammon', 'host': 'fibs.com', 'password': 'hogehoge', """
        r"""'protocol': 'fibs', 'name': 'wxpygammon@fibs.com:4321', 'client_name': """
        r"""'wxPyGammon-alpha-0.1', 'clip_version': '1008', 'port': '4321'}, 'logging': """
        r"""{'format': "'%(asctime)s", 'filename': './wxPyGammon.log', 'filemode': 'w', """
        r"""'level': '10'}, 'CommandDebugger': {'show': 'True'}}>"""))

