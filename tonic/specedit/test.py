#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import StringIO
import unittest

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
    self.assert_(a is not None)
    self.assertEqual(a, text)

  def assertPackageInfo(self, node, name, value):
    self.assertEqual(node.tag, 'package_info')
    self.assertAttribute(node, 'name', name)
    self.assertAttribute(node, 'value', value)

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

    self.assertEqual(len(package), 10 + 1 + 1)
    #first package is main package.
    summary, name, version, release, \
    source, license, group, packager, \
    buildroot, url, comment, \
    description = [n for n in package]

    self.assertPackageInfo(summary,
                        'Summary',
                        "Scheme script interpreter "
                        "with multibyte character handling")
    self.assertPackageInfo(name, 'Name', "Gauche")
    self.assertPackageInfo(version, 'Version', "%{version}")
    self.assertPackageInfo(release, 'Release', "1")
    self.assertPackageInfo(license, 'License', "revised BSD")
    self.assertPackageInfo(group, 'Group', "Development/Languages")
    self.assertPackageInfo(packager, 'Packager', "Shiro Kawai (shiro@acm.org)")
    self.assertPackageInfo(buildroot, 'Buildroot', "%{_tmppath}/rpm")
    self.assertPackageInfo(url, 'URL', "http://practical-scheme.net/gauche/")
    self.assertEqual(comment.text, 'Prefix: /usr')

    self.assertEqual(description.text,
"""Gauche is a Scheme interpreter conforming Revised^5 Report on
Algorithmic Language Scheme.  It is designed for rapid development
of daily tools like system management and text processing.
It can handle multibyte character strings natively.
""")
  def test_package1(self):
    package = self.root.find('package[@name="%{encoding}"]')
    self.assert_(package is not None)
    summary, group, provides, license, requires, \
    description = [n for n in package]
    self.assertPackageInfo(summary, 'Summary',
         "Scheme script interpreter with multibyte "
         "character handling")
    self.assertPackageInfo(group, 'Group', "Development/Languages")
    self.assertPackageInfo(provides, 'Provides', "Gauche libgauche.so")
    self.assertPackageInfo(license, 'License', "revised BSD")
    self.assertPackageInfo(requires, 'Requires', "Gauche-common")
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
    summary, group, license, description = [n for n in package]

    self.assertPackageInfo(summary, 'Summary',
        "Scheme script interpreter with multibyte "
        "character handling")
    self.assertPackageInfo(group, "Group", "Development/Languages")
    self.assertPackageInfo(license, "License", "revised BSD")

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

    self.assertPackageInfo(package[0], 'Summary', "gdbm binding for Gauche Scheme system")
    self.assertPackageInfo(package[1], "Group", "Development/Languages")
    self.assertPackageInfo(package[2], "License", "GPL")
    self.assertPackageInfo(package[3], "Provides", "Gauche-gdbm")
    self.assertPackageInfo(package[4], "Requires", "gdbm >= 1.8.0, Gauche-%{encoding}")
    description = package[5]
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
    print files
    for name, value in files.attrib.items():
      print name, value 
    for n in files:
      print n
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

