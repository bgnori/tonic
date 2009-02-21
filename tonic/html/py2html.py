#!/usrbin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# 2-clause BSD license
# Copyright 2009 Noriyuki Hosaka bgnori@gmail.com
#

import sys
from htmlentitydefs import entitydefs

_d = dict([(value, '&'+key+';') for key, value in entitydefs.items()])


def escape(s):
  return ''.join([_d.get(c, c) for c in s])


def style():
  return  '''\
<style type="text/css">
<!--
body {
    counter-reset: lineno;
}
.codeblock {
    white-space: pre-wrap; /* CSS3 */
    white-space: -moz-pre-wrap; /* Gecho(FireFox, Mozilla) */
    white-space: -o-pre-wrap; /* opera */
    white-space: -pre-wrap; /* old */
    word-wrap: break-wrap; /* IE5.5 or later + Safari */
    background: skyblue; /* debug color */
}
code:before {
    content: 'line:'counter(lineno, decimal-leading-zero)' ';
    counter-increment: lineno;
}
-->
</style>'''

def code_formatter(code):
  return '\n'.join(['<pre class="codeblock">'] 
                 + ['<code>' + escape(line.strip('\n')) + '</code>' for line in code]
                 + ['</pre>']
         )

def convert(i, o, name=None):
  if name is None:
    name = 'unknown python code'
  o.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
  o.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">')
  o.write('<head><title>%s</title>'%name)
  o.write(style())
  o.write('</head>')
  o.write('<body>')
  o.write(code_formatter(i))
  o.write('</body>')
  o.write('</html>')
  o.flush()

if __name__ == '__main__':
  assert len(sys.argv) > 1
  f = file(sys.argv[1])
  try:
    convert(f, sys.stdout)
  finally:
    f.close()

