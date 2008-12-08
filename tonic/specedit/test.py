#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import StringIO

import unittest
import nose

from tonic.funny import LooseQuacker as Mock

from tonic import specedit
from tonic.specedit import base


parser_mock = Mock(subelement=None)
parser_mock.subelement = (lambda s:None)

class SpecTest(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

class LineParserTest(unittest.TestCase):
  def setUp(self):
    self.parser = base.LineParser(parser_mock)
  def tearDown(self):
    pass
  def test_none(self):
    pass
  def test_regexp(self):
    r = self.parser.regexp
    self.assert_(r is not None)
  def test_nullline(self):
    self.parser.parse('')

class ParserTest(unittest.TestCase):
  def setUp(self):
    self.source = file('./tonic/specedit/testdata/gauche.spec')
    self.parser = specedit.Parser()
    self.root = self.parser.parse(self.source)
  def tearDown(self):
    self.source.close()

  def test_none(self):
    pass

  def assertAttribute(self, node, name, text):
    a = node.get(name)
    self.assert_(a)
    self.assertEqual(a, text)

  def assertDefine(self, node, name, value):
    self.assertEqual(node.get('name'), name)
    self.assertEqual(node.get('value'), value)

  def test_head(self):
    head = self.root.find('head')
    self.assert_(head is not None)

    self.assert_(head[0].text.startswith(''' Spec file to build Gauche RPM package'''))

    defines = list(head.findall('define'))
    self.assert_(defines is not None)
    self.assertEqual(len(defines), 3)
    define1, define2, define3 = defines
    self.assertDefine(define1, 'version', '0.8.14')
    self.assertDefine(define2, 'encoding', 'utf8')
    self.assertDefine(define3, 'threads', 'pthreads')


  def test_package(self):
    package = self.root.find('package')
    self.assert_(package is not None)
    self.assertEqual(package.tag, 'package')

    #first package is main package.
    self.assertAttribute(package, 'Summary', 
                        "Scheme script interpreter "
                        "with multibyte character handling")
    self.assertAttribute(package, 'Name', "Gauche")
    self.assertAttribute(package, 'Release', "1")
    self.assertAttribute(package, 'License', "revised BSD")
    self.assertAttribute(package, 'Group', "Development/Languages")
    self.assertAttribute(package, 'Packager', "Shiro Kawai (shiro@acm.org)")
    self.assertAttribute(package, 'Buildroot', "%{_tmppath}/rpm")
    self.assertAttribute(package, 'URL', "http://practical-scheme.net/gauche/")
    

    descriptions = list(package.findall('description'))
    self.assertEqual(len(descriptions), 1)
    description = descriptions[0]
    self.assertEqual(description.text,
"""Gauche is a Scheme interpreter conforming Revised^5 Report on
Algorithmic Language Scheme.  It is designed for rapid development
of daily tools like system management and text processing.
It can handle multibyte character strings natively.
""")
  def test_package1(self):
    package = self.root.find('package[@name="%{encoding}"]')
    self.assert_(package is not None)
    self.assertAttribute(package, 'Summary',
         "Scheme script interpreter with multibyte "
         "character handling")
    self.assertAttribute(package, 'Group', "Development/Languages")
    self.assertAttribute(package, 'Provides', "Gauche libgauche.so")
    self.assertAttribute(package, 'License', "revised BSD")
    self.assertAttribute(package, 'Requires', "Gauche-common")
    description = package.find('description')
    self.assertAttribute(description, 'name', "%{encoding}")
    self.assertEqual(description.text,
"""Gauche is a Scheme interpreter conforming Revised^5 Report on
Algorithmic Language Scheme.  It is designed for rapid development
of daily tools like system management and text processing.
It can handle multibyte character strings natively.
This package is compiled with %{encoding} as the native character encoding.
""")

  def test_package2(self):
    package = self.root.find("package[@name='common']")
    self.assertAttribute(package, 'Summary',
        "Scheme script interpreter with multibyte "
        "character handling")
    self.assertAttribute(package, "Group", "Development/Languages")
    self.assertAttribute(package, "License", "revised BSD")
    description = package.find('description')
    self.assertAttribute(description, 'name', "common")
    self.assertEqual(description.text,
"""Gauche is a Scheme interpreter conforming Revised^5 Report on
Algorithmic Language Scheme.  It is designed for rapid development
of daily tools like system management and text processing.
It can handle multibyte character strings natively.
This package includes common part that is independent from any
native character encoding.  You need either Gauche-eucjp or Gauche-utf8
package as well.
""")

  def test_package3(self):
    package = self.root.find('package[@name="gdbm-%{encoding}"]')
    self.assert_(package is not None)
    self.assertAttribute(package, 'Summary', "gdbm binding for Gauche Scheme system")
    self.assertAttribute(package, "Group", "Development/Languages")
    self.assertAttribute(package, "License", "GPL")
    self.assertAttribute(package, "Provides", "Gauche-gdbm")
    self.assertAttribute(package, "Requires", "gdbm >= 1.8.0, Gauche-%{encoding}")
    description = package.find('description')
    self.assertAttribute(description, 'name', "gdbm-%{encoding}")
    self.assertEqual(description.text, """This package adds gdbm binding to the Gauche Scheme system.\n""")

  def test_prep(self):
    prep = self.root.find("prep")
    self.assert_(prep is not None)
    setup = prep.find('setup')
    self.assert_(setup is not None)

  def test_build(self):
    build = self.root.find("build")
    self.assert_(build is not None)
    step = build.find('step')
    self.assertEqual(step.text, "./configure --prefix=/usr --mandir='${prefix}/share/man' --infodir='${prefix}/share/info' --enable-threads=%{threads} --enable-multibyte=%{encoding}")
    ifarch = build.find('ifarch')
    self.assertAttribute(ifarch, 'cond', 'i386')
    th, el = ifarch
    self.assert_(el is not None)
    self.assert_(th is not None)
    self.assertEqual(len(th), 1)
    self.assertEqual(th[0].tag, 'step')
    self.assertEqual(th[0].text, 'make OPTFLAGS="-fomit-frame-pointer"')
    self.assertEqual(len(el), 1)
    self.assertEqual(el[0].tag, 'step')
    self.assertEqual(el[0].text, 'make')

  def test_install(self):
    install = self.root.find("install")
    self.assert_(install is not None)
    step1, step2, step3 = install.findall('step')
    self.assertEqual(step1.text, "rm -rf ${RPM_BUILD_ROOT}/usr/lib/gauche")
    self.assertEqual(step2.text, "rm -rf ${RPM_BUILD_ROOT}/usr/share/gauche")
    self.assertEqual(step3.text,  "rm -rf ${RPM_BUILD_ROOT}/usr/share/man/man1")

  def test_clean(self):
    clean = self.root.find("clean")
    self.assert_(clean is not None)

  def test_post(self):
    post = self.root.find("post")
    self.assert_(post is not None)

  def test_post2(self):
    post = self.root.find('post[@name="%{encoding}"]')
    self.assert_(post is not None)
    step, = post.findall('step')
    self.assertEqual(step.text,  '''/usr/bin/gosh -u slib -e "(require 'logical)" -e "(exit 0)" > /dev/null 2>&1 || echo''')

  def test_files(self):
    files = self.root.find('files[@name="common"]')
    self.assert_(files is not None)
    self.assertAttribute(files, "option", "-f rpmfiles-common.txt")
    defattr = files.find('defattr')
    self.assert_(defattr is not None)
    self.assertAttribute(defattr, "1", "-")
    self.assertAttribute(defattr, "2", "root")
    self.assertAttribute(defattr, "3", "root")

    doc = files.find('doc')
    f1, f2, f3, f4 ,f5 = doc.findall('file')
    self.assertAttribute(f1, "value", "COPYING")
    self.assertAttribute(f2, "value", "ChangeLog")
    self.assertAttribute(f3, "value", "INSTALL")
    self.assertAttribute(f4, "value", "INSTALL.eucjp")
    self.assertAttribute(f5, "value", "Gauche.spec")

    items = ("/usr/share/info/",
        "/usr/share/man/man1/",
        "/usr/share/gauche/site",
        "/usr/share/aclocal/gauche.m4",
      )
    for i, item in enumerate(files.findall('item')):
      self.assertAttribute(item, "value", items[i])


  def test_files1(self):
    files = self.root.find('files[@name="%{encoding}"]')
    self.assert_(files is not None)
    self.assertAttribute(files, "option", "-f rpmfiles-encoding.txt")
    defattr = files.find('defattr')
    self.assert_(defattr is not None)
    self.assertAttribute(defattr, "1", "-")
    self.assertAttribute(defattr, "2", "root")
    self.assertAttribute(defattr, "3", "root")

    items = ("/usr/bin/gosh",
        "/usr/bin/gauche-config",
        "/usr/bin/gauche-cesconv",
        "/usr/bin/gauche-install",
        "/usr/bin/gauche-package",
        "/usr/lib/libgauche.so",
        "/usr/lib/libgauche.so.0",
        "/usr/lib/libgauche.so.%{version}",
        "/usr/lib/gauche/site/",
     )
    for i, item in enumerate(files.findall('item')):
      self.assertAttribute(item, "value", items[i])

  def test_files2(self):
    files = self.root.find('files[@name="%{encoding}"]')
    self.assert_(files is not None)
    self.assertAttribute(files, "option", "-f rpmfiles-encoding.txt")
    defattr = files.find('defattr')
    self.assertAttribute(defattr, "1", "-")
    self.assertAttribute(defattr, "2", "root")
    self.assertAttribute(defattr, "3", "root")

  def test_files3(self):
    files = self.root.find('files[@name="gdbm-%{encoding}"]')
    self.assert_(files is not None)
    self.assertAttribute(files, "option", "-f rpmfiles-gdbm.txt")

    defattr = files.find('defattr')
    self.assert_(defattr is not None)
    self.assertAttribute(defattr, "1", "-")
    self.assertAttribute(defattr, "2", "root")
    self.assertAttribute(defattr, "3", "root")

  def test_chagelog(self):
    changelog = self.root.find("changelog")
    self.assert_(changelog is not None)
    self.assert_(changelog.text.startswith("""* Mon Oct  6 2008 Shiro Kawai"""))

