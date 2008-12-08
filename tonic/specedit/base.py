#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2008 Noriyuki Hosaka bgnori@gmail.com
#
import StringIO
import pprint
import elementtree.ElementTree as ET

from tonic.lineparser import EMPTY, LineParser

class CommentParser(LineParser):
  name = 'comment'
  _first = (
             r'''(^#(?P<comment>.*))'''
            )
  _last = EMPTY
  def oninit(self):
    self.parent.subelement(self.name)
  def done(self):
    self.parent.pop()
  def handle_comment(self, match, matchobj):
    self.parent.subelement('comment')
    self.parent.current.text = match
    self.parent.pop()

class HeadParser(CommentParser):
  name = 'head'
  _first = ( 
             r'''(?P<define>^%define(\s+)(?P<definename>\w+)(\s+)(?P<definevalue>[a-zA-Z0-9_.-]+))'''
           )
  _last = EMPTY
  def handle_define(self, match, matchobj):
    d = matchobj.groupdict()
    self.parent.subelement('define')
    self.parent.current.attrib['name'] = d['definename']
    self.parent.current.attrib['value'] = d['definevalue']
    self.parent.pop()


class PackageParser(CommentParser):
  name = 'package'
  _first = (
             r'''(^%package( *(?P<package_arg>.*))?)'''
             r'''|'''
             r'''(^Summary: (?P<Summary>.*))'''
             r'''|'''
             r'''(^Name: (?P<Name>.*))'''
             r'''|'''
             r'''(^Version: (?P<Version>.*))'''
             r'''|'''
             r'''(^Release: (?P<Release>.*))'''
             r'''|'''
             r'''(^Source: (?P<Source>.*))'''
             r'''|'''
             r'''(^License: (?P<License>.*))'''
             r'''|'''
             r'''(^Provides: (?P<Provides>.*))'''
             r'''|'''
             r'''(^Requires: (?P<Requires>.*))'''
             r'''|'''
             r'''(^Group: (?P<Group>.*))'''
             r'''|'''
             r'''(^Packager: (?P<Packager>.*))'''
             r'''|'''
             r'''(^Buildroot: (?P<Buildroot>.*))'''
             r'''|'''
             r'''(^URL: (?P<URL>.*))'''
            )
  _last = EMPTY

  def done(self):
    assert self.parent.current.tag == 'package'
    self.parent.last_package = self.parent.current
    CommentParser.done(self)

  def handle_package_arg(self, match, matchobj):
    self.parent.current.attrib['name'] = match

  def handle_Name(self, match, matchobj):
    self.parent.current.attrib['Name'] = match
  def handle_Summary(self, match, matchobj):
    self.parent.current.attrib['Summary'] = match
  def handle_Version(self, match, matchobj):
    self.parent.current.attrib['Version'] = match
  def handle_Release(self, match, matchobj):
    self.parent.current.attrib['Release'] = match
  def handle_Source(self, match, matchobj):
    self.parent.current.attrib['Source'] = match
  def handle_License(self, match, matchobj):
    self.parent.current.attrib['License'] = match
  def handle_Requires(self, match, matchobj):
    self.parent.current.attrib['Requires'] = match
  def handle_Provides(self, match, matchobj):
    self.parent.current.attrib['Provides'] = match
  def handle_Group(self, match, matchobj):
    self.parent.current.attrib['Group'] = match
  def handle_Packager(self, match, matchobj):
    self.parent.current.attrib['Packager'] = match
  def handle_Buildroot(self, match, matchobj):
    self.parent.current.attrib['Buildroot'] = match
  def handle_URL(self, match, matchobj):
    self.parent.current.attrib['URL'] = match

class DescriptionParser(CommentParser):
  name = 'description'
  _first = (
            r'''(^%description( *(?P<description_arg>.*)))'''
           )
  _last = (
            r'''((?P<descriptiontext>^.*))'''
           )
  def oninit(self):
    assert self.parent.last_package is not None
    e = ET.SubElement(self.parent.last_package, 'description')
    self.parent.push(e)
    
  def handle_description_arg(self, match, matchobj):
    self.parent.description.attrib['name'] = match

  def handle_descriptiontext(self, match, matchobj):
    if self.parent.description.text:
      self.parent.description.text += match + '\n'
    else:
      self.parent.description.text = match + '\n'


class StepParser(CommentParser):
  _first = EMPTY
  _last = (
             r'''(?P<step>^.+)'''
          )
  def handle_step(self, match, matchobj):
    self.parent.subelement('step')
    self.parent.current.text = match
    self.parent.pop()


class PrepParser(StepParser):
  name = 'prep'
  _first = (
             r'''(^%prep *(?P<prep>.*))'''
             r'''|'''
             r'''((?P<setup>^%setup) *(?P<setup_arg>.*))'''
            )
  _last = EMPTY
  def handle_prep(self, match, matchobj):
    assert self.parent.current.tag == 'prep'
    self.parent.current.attrib['name'] = match
  def handle_setup(self, match, matchobj):
    d = matchobj.groupdict()
    self.parent.subelement('setup')
    self.parent.current.text = d.get('setup_arg', None)
    self.parent.pop()


class BuildParser(StepParser):
  name = 'build'
  _first = (
             r'''(^%build *(?P<build_arg>.*))'''
             r'''|'''
             r'''((?P<ifarch>^%ifarch) *(?P<cond>.*))'''
             r'''|'''
             r'''(?P<else>^%else)'''
             r'''|'''
             r'''(?P<endif>^%endif)'''
           )
  _last = EMPTY
  def handle_build_arg(self, match, matchobj):
    self.parent.current.attrib['name'] = match
  def handle_ifarch(self, match, matchobj):
    self.parent.subelement('ifarch')
    d = matchobj.groupdict()
    self.parent.current.attrib['cond'] = d['cond']
    self.parent.subelement('then')
  def handle_else(self, match, matchobj):
    assert self.parent.current.tag == 'then'
    self.parent.pop()
    self.parent.subelement('else')
  def handle_endif(self, match, matchobj):
    assert self.parent.current.tag == 'else'
    self.parent.pop()
    assert self.parent.current.tag == 'ifarch'
    self.parent.pop()


class InstallParser(StepParser):
  name = 'install'
  _first = (
             r'''(^%install *(?P<install_arg>.*))'''
           )
  _last = EMPTY
  def handle_install_arg(self, match, matchobj):
    self.parent.current.attrib['name'] = match


class CleanParser(StepParser):
  name = 'clean'
  _first = (
             r'''(^%clean *(?P<clean_arg>.*))'''
           )
  _last = EMPTY
  def handle_clean_arg(self, match, matchobj):
    self.parent.current.attrib['name'] = match


class PostParser(StepParser):
  name = 'post'
  _first = (
             r'''(^%post *(?P<post_arg>.*))'''
            )
  _last = EMPTY
  def handle_post_arg(self, match, matchobj):
    self.parent.current.attrib['name'] = match


class FilesParser(CommentParser):
  name = 'files'
  _first =  (
      r'''(^%files *(?P<files_arg>[^ ]*) *(?P<files_option>.*))'''
      r'''|'''
      r'''(^%doc +(?P<doc>(([0-9a-zA-Z.-]+) ?)+))'''
      r'''|'''
      r'''(?P<defattr>^%defattr)'''
      r'''\('''
        r'''(?P<arg1>[^,]+),'''
        r'''(?P<arg2>[^,]+),'''
        r'''(?P<arg3>[^)]+)'''
      r'''\)'''
      r'''|'''
      r'''(?P<path>^(/[a-zA-Z0-9._%{}-]+)+/?)'''
      )
  _last = EMPTY
  def handle_files_arg(self, match, matchobj):
    self.parent.current.attrib['name'] = match
  def handle_files_option(self, match, matchobj):
    self.parent.current.attrib['option'] = match
  def handle_doc(self, match, matchobj):
    assert self.parent.current.tag == 'files'
    self.parent.subelement('doc')
    for v in match.split():
      self.parent.subelement('file')
      self.parent.current.attrib['value'] = v
      self.parent.pop()
    self.parent.pop()

  def handle_defattr(self, match, matchobj):
    assert self.parent.current.tag == 'files'
    self.parent.subelement('defattr')
    d = matchobj.groupdict()
    self.parent.current.attrib['1'] = d['arg1']
    self.parent.current.attrib['2'] = d['arg2']
    self.parent.current.attrib['3'] = d['arg3']
    self.parent.pop()
  def handle_path(self, match, matchobj):
    assert self.parent.current.tag == 'files'
    self.parent.subelement('item')
    self.parent.current.attrib['value'] = match
    self.parent.pop()


class ChangeLogParser(CommentParser):
  name = 'changelog'
  _first = r'''(^%changelog *(?P<changelog_arg>.*))'''
  _last = r'(?P<text>^.*$)'
  def handle_changelog_arg(self, match, matchobj):
    assert self.parent.current.tag == 'changelog'
    self.parent.current.attrib['name'] = match
  def handle_text(self, match, matchobj):
    assert self.parent.current.tag == 'changelog'
    if self.parent.current.text:
      self.parent.current.text += (match + '\n')
    else:
      self.parent.current.text = match + '\n'


def makebundle():
  d = dict()
  for key, item in globals().items():
    if isinstance(item, type) and issubclass(item, LineParser):
      d.update({item.name: item})
  return d
  

class Parser(object):
  def __init__(self, debug=None):
    self.debug = debug
    self.parsers = makebundle()
    self.reset()

  def reset(self):
    self.prev_line = None
    self.curr_line = None
    self.last_package = None
    self.current_parser = None
    self.stack = []
    self.push(ET.Element('spec'))
    self.current_parser = HeadParser(self, self.debug)

  def get_current(self):
    return self.stack[-1]
  current = property(get_current, None, None)

  def subelement(self, name):
    if self.debug:
      print 'node:', self.current, '->', name
      pprint.pprint(('prev', self.prev_line))
      pprint.pprint(('curr', self.curr_line))
      print '  by:', self.current_parser
    sub =  ET.SubElement(self.current, name)
    self.push(sub)
    assert sub == self.current
    return sub

  def get_description(self):
    pkgs = list(self.stack[0].findall(".//package"))
    assert pkgs
    package = pkgs[-1]
    descriptions = list(package.findall("description"))
    assert len(descriptions) == 1
    return descriptions[0]
  description = property(get_description, None, None)

  def pop(self):
    if self.debug:
      print 'pop :', self.stack[-1], self.stack[-1].attrib
    self.stack.pop(-1)

  def push(self, node):
    if self.debug:
      print 'push:',node
    self.stack.append(node)


  def is_start_of_package(self, line):
    if not line:
      return False
    for matchobj in PackageParser.regexp.finditer(line):
      for name, match in matchobj.groupdict().items():
        assert isinstance(name, str)
        if name != 'comment' and match is not None:
          return True
    return False

  def parse(self, f):
    self.reset()
    try:
      for i, line in enumerate(f):
        self.curr_line = line
        if isinstance(self.current_parser, HeadParser)\
          and self.is_start_of_package(line):
          klass = PackageParser
          if self.debug:
            print 'end of head, starting', klass
            print line
          self.current_parser.done()
          self.current_parser = klass(self, self.debug)

        elif line.startswith('%'):
          head = line.split()[0]
          klass = self.parsers.get(head[1:], None)
          if klass:
            assert head[1:] != 'define'
            if self.debug:
              print 'starting:', klass
            self.current_parser.done()
            self.current_parser = klass(self, self.debug)
        self.current_parser.parse(line)
        self.prev_line = line
    except Exception, e:
      print 'something wrong around line', i+1
      pprint.pprint((i, self.prev_line))
      pprint.pprint((i+1, self.curr_line))
      raise
    self.current_parser.done()
    assert len(self.stack) == 1 #just root is there.
    return self.current

  
class Writer(object):
  def __init__(self):
    pass

  def write(self, t, f):
    handler_name = 'handle_' + t.tag
    handler = getattr(self, handler_name, None)
    assert handler, handler_name
    handler(t, f)
    for c in t:
      self.write(c, f)

  def handle_spec(self, t, f):pass
  def handle_head(self, t, f):pass
  def handle_package(self, t, f):
    name = t.get('name', None)
    if name:
      f.write('%%package %s\n'%name)
    else:
      pass #main package
    for name, value in t.attrib.items():
      if name[0].isupper():
        f.write('%s: %s\n'%(name, value))

  def handle_comment(self, t, f):
    f.write('#%s\n'%t.text)
  def handle_define(self, t, f):
    f.write('%%define %s %s\n'%(t.attrib['name'], t.attrib['value']))
  def handle_description(self, t, f):
    name = t.get('name', None)
    if name:
      f.write('%%description %s\n'%name)
    else:
      f.write('%description\n')
    if t.text is not None:
      f.write(t.text)

    f.write('\n')

  def handle_prep(self, t, f):
    name = t.get('name', None)
    if name:
      f.write('%%prep %s\n'%name)
    else:
      f.write('%prep\n')

  def handle_setup(self, t, f):
    arg = t.text
    if arg:
      f.write('%%setup %s\n'%arg)
    else:
      f.write('%setup\n')

  def handle_build(self, t, f):
    name = t.get('name', None)
    if name:
      f.write('%%build %s\n'%name)
    else:
      f.write('%build\n')
  def handle_ifarch(self, t, f):
    cond = t.get('cond', None)
    assert cond
    f.write('%%ifarch %s\n'%cond)

  def handle_then(self, t, f):pass
  def handle_else(self, t, f):
    f.write('%else\n')
  def handle_endif(self, t, f):
    f.write('%endif\n')

  def handle_step(self, t, f):
    f.write('%s\n'%t.text)

  def handle_install(self, t, f):
    name = t.get('name', None)
    if name:
      f.write('%%install %s\n'%name)
    else:
      f.write('%install\n')

  def handle_clean(self, t, f):
    name = t.get('name', None)
    if name:
      f.write('%%clean %s\n'%name)
    else:
      f.write('%clean\n')

  def handle_post(self, t, f):
    name = t.get('name', None)
    if name:
      f.write('%%post %s\n'%name)
    else:
      f.write('%post\n')

  def handle_files(self, t, f):
    name = t.get('name', None)
    if name:
      f.write('%%files %s\n'%name)
    else:
      f.write('%files\n')

  def handle_defattr(self, t, f):
    f.write('%%defattr(%s,%s,%s)\n'%\
              (t.attrib['1'], t.attrib['2'], t.attrib['3']))

  def handle_doc(self, t, f):
      s = ' '.join([c.get('value') for c in t])
      f.write('%%doc %s\n'%s)

  def handle_file(self, t, f):pass
  def handle_item(self, t, f):
    path = t.get('value', None)
    assert path
    f.write('%s\n'%path)

  def handle_changelog(self, t, f):
    name = t.get('name', None)
    if name:
      f.write('%%changelog %s\n'%name)
    else:
      f.write('%changelog\n')
    if t.text is not None:
      f.write(t.text)
    f.write('\n')

class SpecFile(StringIO.StringIO):
  def __init__(self, filename, buf=None):
    StringIO.StringIO.__init__(self, buf)
    self.name = filename

