%{!?__python_ver:%define __python_ver EMPTY}
%define unicode ucs4

%if "%{__python_ver}" != "EMPTY"
%define main_python 0
%define python python%{__python_ver}
%define tkinter tkinter%{__python_ver}
%else
%define main_python 1
%define python python
%define tkinter tkinter
%endif

%define pybasever 2.4
%define jp_codecs 1.4.11
%define tools_dir %{_libdir}/python%{pybasever}/Tools
%define demo_dir %{_libdir}/python%{pybasever}/Demo
%define doc_tools_dir %{_libdir}/python%{pybasever}/Doc/tools

Summary: An interpreted, interactive, object-oriented programming language.
Name: %{python}
Version: %{pybasever}.3
Release: 21%{?dist}
License: PSF - see LICENSE
Group: Development/Languages
Provides: python-abi = %{pybasever}
Provides: python(abi) = %{pybasever}
# optik is part of python 2.3 as optparse
Provides: python-optik = 1.4.1
Obsoletes: python-optik
Source: http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2
Source5: http://www.python.jp/pub/JapaneseCodecs/JapaneseCodecs-%{jp_codecs}.tar.gz
Source6: http://gigue.peabody.jhu.edu/~mdboom/omi/source/shm_source/shmmodule.c
Source7: python-2.3.4-optik.py

Patch0: python-2.4.3-config.patch
Patch3: Python-2.2.1-pydocnogui.patch
Patch7: python-2.3.4-lib64-regex.patch
Patch8: python-2.4.1-lib64.patch
Patch9: japanese-codecs-lib64.patch
Patch13: python-2.4-distutils-bdist-rpm.patch
Patch14: python-2.3.4-pydocnodoc.patch
Patch15: python-2.4.1-canonicalize.patch
Patch16: python-2.4-gen-assert.patch
Patch17: python-2.4-webbrowser.patch
Patch18: python-2.4.3-cflags.patch
Patch19: python-2.4.3-locale.patch
Patch20: python-2.4.3-unicodeobject.patch
Patch21: python-syslog-fail-noatexittb.patch
Patch22: python-2.5.CVE-2007-4965-int-overflow.patch
Patch23: python-httplib-chunked.patch

%if %{main_python}
Obsoletes: Distutils
Provides: Distutils
Obsoletes: python2 
Provides: python2 = %{version}
BuildPrereq: db4-devel >= 4.3
%else
#BuildPrereq: db3-devel
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildPrereq: readline-devel, libtermcap-devel, openssl-devel, gmp-devel
BuildPrereq: ncurses-devel, gdbm-devel, zlib-devel, expat-devel
BuildPrereq: libGL-devel tk tix gcc-c++ libX11-devel glibc-devel
BuildPrereq: bzip2 tar /usr/bin/find pkgconfig tcl-devel tk-devel
BuildPrereq: tix-devel bzip2-devel
BuildPrereq: autoconf
URL: http://www.python.org/

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface. This package contains most of the standard
Python modules, as well as modules for interfacing to the Tix widget
set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.

%package devel
Summary: The libraries and header files needed for Python development.
Group: Development/Libraries
Requires: %{python} = %{version}-%{release}
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: %{python} < %{version}-%{release}
%if %{main_python}
Obsoletes: python2-devel
Provides: python2-devel = %{version}-%{release}
%endif

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package tools
Summary: A collection of development tools included with Python.
Group: Development/Tools
Requires: %{name} = %{version}-%{release}
Requires: %{tkinter} = %{version}-%{release}
%if %{main_python}
Obsoletes: python2-tools
Provides: python2-tools = %{version}
%endif

%description tools
The Python package includes several development tools that are used
to build python programs.

%package -n %{tkinter}
Summary: A graphical user interface for the Python scripting language.
Group: Development/Languages
BuildPrereq:  tcl, tk
Requires: %{name} = %{version}-%{release}
%if %{main_python}
Obsoletes: tkinter2
Provides: tkinter2 = %{version}
%endif

%description -n %{tkinter}

The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%prep
%setup -q -n Python-%{version} -a 5

%patch0 -p1 -b .rhconfig
%patch3 -p1 -b .no_gui
%if %{_lib} == lib64
%patch7 -p1 -b .lib64-regex
%patch8 -p1 -b .lib64
%patch9 -p0 -b .lib64-j
%endif
%patch13 -p1 -b .bdist-rpm
%patch14 -p1 -b .no-doc
%patch15 -p1 -b .canonicalize
%patch16 -p2 -b .gen-assert
%patch17 -p0 -b .web-browser
%patch18 -p1 -b .cflags
%patch19 -p2 -b .locale
%patch20 -p3 -b .unicode-repr
%patch21 -p1 -b .syslog-atexit
%patch22 -p1 -b .CVE-2007-4965-int-overflow
%patch23 -p0 -b .httplib

# This shouldn't be necesarry, but is right now (2.2a3)
find -name "*~" |xargs rm -f

# Temporary workaround to avoid confusing find-requires: don't ship the tests
# as executable files
chmod 0644 Lib/test/test_*.py

# shm module
cp %{SOURCE6} Modules
cat >> Modules/Setup.dist << EOF

# Shared memory module
shm shmmodule.c
EOF

# Backwards compatible optik
install -m 0644 %{SOURCE7} Lib/optik.py

%build
topdir=`pwd`
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC"
export OPT="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC"
export LINKCC="gcc"
if pkg-config openssl ; then
	export CFLAGS="$CFLAGS `pkg-config --cflags openssl`"
	export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi
# Force CC
export CC=gcc
# For patch 15, need to get a newer configure generated out of configure.in
autoconf
%configure --enable-ipv6 --enable-unicode=%{unicode} --enable-shared

make OPT="$CFLAGS" %{?_smp_mflags}
LD_LIBRARY_PATH=$topdir $topdir/python Tools/scripts/pathfix.py -i "%{_bindir}/env python%{pybasever}" .
make OPT="$CFLAGS" %{?_smp_mflags}

%install
[ -d $RPM_BUILD_ROOT ] && rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr $RPM_BUILD_ROOT%{_mandir}

# Clean up patched .py files that are saved as .lib64
for f in distutils/command/install distutils/sysconfig; do
    rm -f Lib/$f.py.lib64
done

make install DESTDIR=$RPM_BUILD_ROOT
# Fix the interpreter path in binaries installed by distutils 
# (which changes them by itself)
# Make sure we preserve the file permissions
for fixed in $RPM_BUILD_ROOT%{_bindir}/pydoc; do
    sed 's,#!.*/python$,#!%{_bindir}/env python%{pybasever},' $fixed > $fixed- \
        && cat $fixed- > $fixed && rm -f $fixed-
done

%if %{main_python}
ln -s python $RPM_BUILD_ROOT%{_bindir}/python2
%else
mv $RPM_BUILD_ROOT%{_bindir}/python $RPM_BUILD_ROOT%{_bindir}/%{python}
mv $RPM_BUILD_ROOT/%{_mandir}/man1/python.1 $RPM_BUILD_ROOT/%{_mandir}/man1/python%{pybasever}.1
%endif

# tools

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/python%{pybasever}/site-packages

#modulator
cat > ${RPM_BUILD_ROOT}%{_bindir}/modulator << EOF
#!/bin/bash
exec %{_libdir}/python%{pybasever}/site-packages/modulator/modulator.py
EOF
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/modulator
cp -r Tools/modulator \
  ${RPM_BUILD_ROOT}%{_libdir}/python%{pybasever}/site-packages/

#pynche
cat > ${RPM_BUILD_ROOT}%{_bindir}/pynche << EOF
#!/bin/bash
exec %{_libdir}/python%{pybasever}/site-packages/pynche/pynche
EOF
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/pynche
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche \
  ${RPM_BUILD_ROOT}%{_libdir}/python%{pybasever}/site-packages/

mv Tools/modulator/README Tools/modulator/README.modulator
mv Tools/pynche/README Tools/pynche/README.pynche

#gettext
install -m755  Tools/i18n/pygettext.py $RPM_BUILD_ROOT%{_bindir}/
install -m755  Tools/i18n/msgfmt.py $RPM_BUILD_ROOT%{_bindir}/

# Useful development tools
install -m755 -d $RPM_BUILD_ROOT%{tools_dir}/scripts
install Tools/README $RPM_BUILD_ROOT%{tools_dir}/
install Tools/scripts/*py $RPM_BUILD_ROOT%{tools_dir}/scripts/

# Documentation tools
install -m755 -d $RPM_BUILD_ROOT%{doc_tools_dir}
install -m755 Doc/tools/mkhowto $RPM_BUILD_ROOT%{doc_tools_dir}

# Useful demo scripts
install -m755 -d $RPM_BUILD_ROOT%{demo_dir}
cp -ar Demo/* $RPM_BUILD_ROOT%{demo_dir}

# Get rid of crap
find $RPM_BUILD_ROOT/ -name "*~"|xargs rm -f
find $RPM_BUILD_ROOT/ -name ".cvsignore"|xargs rm -f
find . -name "*~"|xargs rm -f
find . -name ".cvsignore"|xargs rm -f
#zero length
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{pybasever}/site-packages/modulator/Templates/copyright

# Clean up the testsuite - we don't need compiled files for it
find $RPM_BUILD_ROOT%{_libdir}/python%{pybasever}/test \
    -name "*.pyc" -o -name "*.pyo" | xargs rm -f
rm -f $RPM_BUILD_ROOT%{_libdir}/python2.2/LICENSE.txt


#make the binaries install side by side with the main python
%if !%{main_python}
pushd $RPM_BUILD_ROOT%{_bindir}
mv idle idle%{__python_ver}
mv modulator modulator%{__python_ver}
mv pynche pynche%{__python_ver}
mv pygettext.py pygettext%{__python_ver}.py
mv msgfmt.py msgfmt%{__python_ver}.py
mv smtpd.py smtpd%{__python_ver}.py
mv pydoc pydoc%{__python_ver}
popd
%endif

# Japanese codecs
pushd JapaneseCodecs-%{jp_codecs}
# We need to set LD_LIBRARY_PATH since python is now compiled as shared, and
# we always want to use the currently compiled one
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
    ../python setup.py install --root=$RPM_BUILD_ROOT
popd

find $RPM_BUILD_ROOT%{_libdir}/python%{pybasever}/lib-dynload -type d | sed "s|$RPM_BUILD_ROOT|%dir |" > dynfiles
find $RPM_BUILD_ROOT%{_libdir}/python%{pybasever}/lib-dynload -type f | grep -v "_tkinter.so$" | sed "s|$RPM_BUILD_ROOT||" >> dynfiles

# Fix for bug #136654
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{pybasever}/email/test/data/audiotest.au $RPM_BUILD_ROOT%{_libdir}/python%{pybasever}/test/audiotest.au

# Fix bug #143667: python should own /usr/lib/python2.x on 64-bit machines
%if %{_lib} == lib64
install -d $RPM_BUILD_ROOT/usr/lib/python%{pybasever}/site-packages
%endif

# Make python-devel multilib-ready (bug #192747, #139911)
%define _pyconfig32_h pyconfig-32.h
%define _pyconfig64_h pyconfig-64.h

%ifarch ppc64 s390x x86_64 ia64
%define _pyconfig_h %{_pyconfig64_h}
%else
%define _pyconfig_h %{_pyconfig32_h}
%endif
mv $RPM_BUILD_ROOT%{_includedir}/python%{pybasever}/pyconfig.h \
   $RPM_BUILD_ROOT%{_includedir}/python%{pybasever}/%{_pyconfig_h}
cat > $RPM_BUILD_ROOT%{_includedir}/python%{pybasever}/pyconfig.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_pyconfig32_h}"
#elif __WORDSIZE == 64
#include "%{_pyconfig64_h}"
#else
#error "Unknown word size"
#endif
EOF

# Fix for bug 201434: make sure distutils looks at the right pyconfig.h file
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" $RPM_BUILD_ROOT%{_libdir}/python%{pybasever}/distutils/sysconfig.py

%clean
rm -fr $RPM_BUILD_ROOT

%files -f dynfiles
%defattr(-, root, root)
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/python*
%{_mandir}/*/*
%{_libdir}/libpython%{pybasever}.so*

%dir %{_libdir}/python%{pybasever}
%{_libdir}/python%{pybasever}/site-packages/japanese.pth
%dir %{_libdir}/python%{pybasever}/site-packages
%{_libdir}/python%{pybasever}/site-packages/japanese
%{_libdir}/python%{pybasever}/site-packages/README
%{_libdir}/python%{pybasever}/LICENSE.txt
%{_libdir}/python%{pybasever}/*.py*
%{_libdir}/python%{pybasever}/*.doc
%{_libdir}/python%{pybasever}/bsddb
%dir %{_libdir}/python%{pybasever}/config
%{_libdir}/python%{pybasever}/config/Makefile
%{_libdir}/python%{pybasever}/curses
%{_libdir}/python%{pybasever}/distutils
%{_libdir}/python%{pybasever}/encodings
%{_libdir}/python%{pybasever}/idlelib
%{_libdir}/python%{pybasever}/lib-old
%{_libdir}/python%{pybasever}/logging
%{_libdir}/python%{pybasever}/xml
%{_libdir}/python%{pybasever}/email
%{_libdir}/python%{pybasever}/compiler
%{_libdir}/python%{pybasever}/plat-linux2
%{_libdir}/python%{pybasever}/hotshot
%if %{_lib} == lib64
%attr(0755,root,root) %dir /usr/lib/python%{pybasever}
%attr(0755,root,root) %dir /usr/lib/python%{pybasever}/site-packages
%endif

%files devel
%defattr(-,root,root)
/usr/include/*
%{_libdir}/python%{pybasever}/config
%{_libdir}/python%{pybasever}/test

%files tools
%defattr(-,root,root,755)
%doc Tools/modulator/README.modulator
%doc Tools/pynche/README.pynche
%{_libdir}/python%{pybasever}/site-packages/modulator
%{_libdir}/python%{pybasever}/site-packages/pynche
%{_bindir}/smtpd*.py*
%{_bindir}/idle*
%{_bindir}/modulator*
%{_bindir}/pynche*
%{_bindir}/pygettext*.py*
%{_bindir}/msgfmt*.py*
%{tools_dir}
%{demo_dir}
%{_libdir}/python%{pybasever}/Doc

%files -n %{tkinter}
%defattr(-,root,root,755)
%{_libdir}/python%{pybasever}/lib-tk
%{_libdir}/python%{pybasever}/lib-dynload/_tkinter.so

%changelog
* Mon Jan 14 2008 James Antill <james.antill@redhat.com> - 2.4.3-21
- Fix httplib chunked encoding issues.
- Resolves: rhbz#212019

* Fri Nov  9 2007 James Antill <james.antill@redhat.com> - 2.4.3-20
- Fix CVE-2007-4965 int-overflow for some image operations

* Mon Dec 11 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-19
- fix atexit handler with syslog logging (#218214)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.4.3-18
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-17
- Fixed bug #208166 / CVE-2006-4980: repr unicode buffer overflow

* Thu Aug 17 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-15
- Fixed bug #201434 (distutils.sysconfig is confused by the change to make
  python-devel multilib friendly)

* Fri Jul 21 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-14
- Fixed bug #198971 (case conversion not locale safe in logging library)

* Thu Jul 20 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-13
- Fixed bug #199373 (on some platforms CFLAGS is needed when linking)

* Mon Jul 17 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-12
- added dist tag back

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.4.3-11.FC6.1
- rebuild

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-11.FC6
- and fix it for real

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-10.FC6
- fix python-devel on ia64

* Tue Jun 13 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-9
- Fixed python-devel to be multilib friendly (bug #192747, #139911)

* Tue Jun 13 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-8
- Only copying mkhowto from the Docs - we don't need perl dependencies from
  python-tools.

* Mon Jun 12 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-7
- Fixed bug #121198 (webbrowser.py should use the user's preferences first)

* Mon Jun 12 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-6
- Fixed bug #192592 (too aggressive assertion fails) - SF#1257960
- Fixed bug #167468 (Doc/tools not included) - added in the python-tools package

* Thu Jun  8 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-5
- Fixed bug #193484 (added pydoc in the main package)

* Mon Jun  5 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-4
- Added dist in the release

* Mon May 15 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-3
- rebuilt to fix broken libX11 dependency

* Wed Apr 12 2006 Jeremy Katz <katzj@redhat.com> - 2.4.3-2
- rebuild with new gcc to fix #188649

* Thu Apr  6 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-1
- Updated to 2.4.3

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-3.2.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Mihai Ibanescu <misa@redhat.com> - 2.4.3-3.2
- rebuilt for newer tix

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.2-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Mihai Ibanescu <misa@redhat.com> 2.4.2-3
- fixed #136654 for another instance of audiotest.au

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 19 2005 Bill Nottingham <notting@redhat.com> 2.4.2-2
- fix build for modular X, remove X11R6 path references

* Tue Nov 15 2005 Mihai Ibanescu <misa@redhat.com> 2.4.2-1
- Upgraded to 2.4.2
- BuildRequires autoconf

* Wed Nov  9 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-16
- Rebuilding against newer openssl.
- XFree86-devel no longer exists

* Mon Sep 26 2005 Peter Jones <pjones@redhat.com> 2.4.1-14
- Once more -- this time, to fix -EPERM when you run it in a directory
  you can't read from.

* Mon Sep 26 2005 Peter Jones <pjones@redhat.com> 2.4.1-13
- So, 5 or 6 people have said it works for them with this patch...

* Sun Sep 25 2005 Peter Jones <pjones@redhat.com> 2.4.1-12
- Fixed bug #169159 (check for argc>0 and argv[0] == NULL, not just
    argv[0][0]='\0')
  Reworked the patch from -8 a bit more.

* Fri Sep 23 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-10
- Fixed bug #169159 (don't let python core dump if no arguments are passed in)
  Reworked the patch from -8 a bit more.

* Thu Sep 22 2005 Peter Jones <pjones@redhat.com> 2.4.1-8
- Fix bug #169046 more correctly.

* Thu Sep 22 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-7
- Fixed bug #169046 (realpath is unsafe); thanks to 
  Peter Jones <pjones@redhat.com> and Arjan van de Ven <arjanv@redhat.com> for
  diagnosing and the patch.

* Tue Sep 20 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-4
- Fixed bug #168655 (fixes for building as python24)

* Tue Jul 26 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-3
- Fixed bug #163435 (pynche doesn't start))

* Wed Apr 20 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-2
- Fixed bug #143667 (python should own /usr/lib/python* on 64-bit systems, for
  noarch packages)
- Fixed bug #143419 (BuildRequires db4 is not versioned)

* Wed Apr  6 2005 Mihai Ibanescu <misa@redhat.com> 2.4.1-1
- updated to 2.4.1

* Mon Mar 14 2005 Mihai Ibanescu <misa@redhat.com> 2.4-6
- building the docs from a different source rpm, to decouple bootstrapping
  python from having tetex installed

* Fri Mar 11 2005 Dan Williams <dcbw@redhat.com> 2.4-5
- Rebuild to pick up new libssl.so.5

* Wed Feb  2 2005 Mihai Ibanescu <misa@redhat.com> 2.4-4
- Fixed security issue in SimpleXMLRPCServer.py (#146647)

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 2.4-3
- Rebuilt for new readline.

* Mon Dec  6 2004 Jeff Johnson <jbj@jbj.org> 2.4-2
- db-4.3.21 returns DB_BUFFER_SMALL rather than ENOMEM (#141994).
- add Provide: python(abi) = 2.4
- include msgfmt/pygettext *.pyc and *.pyo from brp-python-bytecompile.

* Fri Dec  3 2004 Mihai Ibanescu <misa@redhat.com> 2.4-1
- Python-2.4.tar.bz2 (final)

* Fri Nov 19 2004 Mihai Ibanescu <misa@redhat.com> 2.4-0.c1.1
- Python-2.4c1.tar.bz2 (release candidate 1)

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 2.4-0.b2.4
- rebuild against db-4.3.21.

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 2.4-0.b2.3
- fix the lib64 patch so that 64bit arches still look in /usr/lib/python...

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 2.4-0.b2.2
- cryptmodule still needs -lcrypt (again)

* Thu Nov  4 2004 Mihai Ibanescu <misa@redhat.com> 2.4-0.b2.1
- Updated to python 2.4b2 (and labeled it 2.4-0.b2.1 to avoid breaking rpm's
  version comparison)

* Thu Nov  4 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-13
- Fixed bug #138112 (python overflows stack buffer) - SF bug 105470

* Tue Nov  2 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-12
- Fixed bugs #131439 #136023 #137863 (.pyc/.pyo files had the buildroot added)

* Tue Oct 26 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-11
- Fixed bug #136654 (python has sketchy audio clip)

* Tue Aug 31 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-10
- Fixed bug #77418 (Demo dir not packaged)
- More tweaking on #19347 (Moved Tools/ under /usr/lib/python2.3/Tools)

* Fri Aug 13 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-8
- Fixed bug #129769: Makefile in new python conflicts with older version found
  in old python-devel
- Reorganized the spec file to get rid of the aspython2 define; __python_ver
  is more powerful.

* Tue Aug  3 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-7
- Including html documentation for non-i386 arches
- Fixed #125362 (python-doc html files have japanese character encoding)
- Fixed #128923 (missing dependency between python and python-devel)

* Fri Jul 30 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-6
- Fixed #128030 (help() not printing anything)
- Fixed #125472 (distutils.sysconfig.get_python_lib() not returning the right
  path on 64-bit systems)
- Fixed #127357 (building python as a shared library)
- Fixed  #19347 (including the contents of Tools/scripts/ in python-tools)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-3
- Added an optik.py that provides the same interface from optparse for
  backward compatibility; obsoleting python-optik

* Mon Jun  7 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-2
- Patched bdist_rpm to allow for builds of multiple binary rpms (bug #123598)

* Fri Jun  4 2004 Mihai Ibanescu <misa@redhat.com> 2.3.4-1
- Updated to 2.3.4-1 with Robert Scheck's help (bug #124764)
- Added BuildRequires: tix-devel (bug #124918)

* Fri May  7 2004 Mihai Ibanescu <misa@redhat.com> 2.3.3-6
- Correct fix for #122304 from upstream:
  http://sourceforge.net/tracker/?func=detail&atid=105470&aid=931848&group_id=5470

* Thu May  6 2004 Mihai Ibanescu <misa@redhat.com> 2.3.3-4
- Fix for bug #122304 : splitting the domain name fails on 64-bit arches
- Fix for bug #120879 : including Makefile into the main package

- Requires XFree86-devel instead of -libs (see bug #118442)

* Tue Mar 16 2004 Mihai Ibanescu <misa@redhat.com> 2.3.3-3
- Requires XFree86-devel instead of -libs (see bug #118442)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec 19 2003 Jeff Johnson <jbj@jbj.org> 2.3.3-1
- upgrade to 2.3.3.

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 2.3.2-9
- rebuild against db-4.2.52.

* Fri Dec 12 2003 Jeremy Katz <katzj@redhat.com> 2.3.2-8
- more rebuilding for new tcl/tk

* Wed Dec  3 2003 Jeff Johnson <jbj@jbj.org> 2.3.2-7.1
- rebuild against db-4.2.42.

* Fri Nov 28 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-7
- rebuilt against newer tcl/tk

* Mon Nov 24 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-6
- added a Provides: python-abi

* Wed Nov 12 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-5
- force CC (#109268)

* Sun Nov  9 2003 Jeremy Katz <katzj@redhat.com> 2.3.2-4
- cryptmodule still needs -lcrypt

* Wed Nov  5 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-2
- Added patch for missing mkhowto

* Thu Oct 16 2003 Mihai Ibanescu <misa@redhat.com> 2.3.2-1
- Updated to 2.3.2

* Thu Sep 25 2003 Mihai Ibanescu <misa@redhat.com> 2.3.1-1
- 2.3.1 final

* Tue Sep 23 2003 Mihai Ibanescu <misa@redhat.com> 2.3.1-0.8.RC1
- Building the python 2.3.1 release candidate
- Updated the lib64 patch

* Wed Jul 30 2003 Mihai Ibanescu <misa@redhat.com> 2.3-0.2
- Building python 2.3
- Added more BuildRequires
- Updated the startup files for modulator and pynche; idle installs its own
  now.

* Thu Jul  3 2003 Mihai Ibanescu <misa@redhat.com> 2.2.3-4
- Rebuilt against newer db4 packages (bug #98539)

* Mon Jun 9 2003 Elliot Lee <sopwith@redhat.com> 2.2.3-3
- rebuilt

* Wed Jun  7 2003 Mihai Ibanescu <misa@redhat.com> 2.2.3-2
- Rebuilt

* Tue Jun  6 2003 Mihai Ibanescu <misa@redhat.com> 2.2.3-1
- Upgraded to 2.2.3

* Wed Apr  2 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-28
- Rebuilt

* Wed Apr  2 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-27
- Modified the ftpuri patch conforming to http://ietf.org/rfc/rfc1738.txt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-25
- Fixed bug #84886: pydoc dies when run w/o arguments
- Fixed bug #84205: add python shm module back (used to be shipped with 1.5.2)
- Fixed bug #84966: path in byte-compiled code still wrong

* Thu Feb 20 2003 Jeremy Katz <katzj@redhat.com> 2.2.2-23
- ftp uri's should be able to specify being rooted at the root instead of 
  where you login via ftp (#84692)

* Mon Feb 10 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-22
- Using newer Japanese codecs (1.4.9). Thanks to 
  Peter Bowen <pzb@datastacks.com> for pointing this out.

* Thu Feb  6 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-21
- Rebuild

* Wed Feb  5 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-20
- Release number bumped really high: turning on UCS4 (ABI compatibility
  breakage)

* Fri Jan 31 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-13
- Attempt to look both in /usr/lib64 and /usr/lib/python2.2/site-packages/:
  some work on python-2.2.2-lib64.patch

* Thu Jan 30 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-12
- Rebuild to incorporate the removal of .lib64 and - files.

* Thu Jan 30 2003 Mihai Ibanescu <misa@redhat.com> 2.2.2-11.7.3
- Fixed bug #82544: Errata removes most tools
- Fixed bug #82435: Python 2.2.2 errata breaks redhat-config-users
- Removed .lib64 and - files that get installed after we fix the multilib
  .py files.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Jens Petersen <petersen@redhat.com> 2.2.2-10
- rebuild to update tkinter's tcltk deps
- convert changelog to utf-8

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.2.2-9
- rebuild

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- pick up OpenSSL cflags and ldflags from pkgconfig if available

* Thu Jan  2 2003 Jeremy Katz <katzj@redhat.com> 2.2.2-8
- urllib2 didn't support non-anonymous ftp.  add support based on how 
  urllib did it (#80676, #78168)

* Mon Dec 16 2002 Mihai Ibanescu <misa@redhat.com> 2.2.2-7
- Fix bug #79647 (Rebuild of SRPM fails if python isn't installed)
- Added a bunch of missing BuildRequires found while fixing the
  above-mentioned bug

* Tue Dec 10 2002 Tim Powers <timp@redhat.com> 2.2.2-6
- rebuild to fix broken tcltk deps for tkinter

* Fri Nov 22 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-3.7.3
- Recompiled for 7.3 (to fix the -lcrypt bug)
- Fix for the spurious error message at the end of the build (build-requires
  gets confused by executable files starting with """"): make the tests
  non-executable.

* Wed Nov 20 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-5
- Fixed configuration patch to add -lcrypt when compiling cryptmodule.c

2.2.2-4
- Spec file change from Matt Wilson <msw@redhat.com> to disable linking 
  with the C++ compiler.

* Mon Nov 11 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-3.*
- Merged patch from Karsten Hopp <karsten@redhat.de> from 2.2.1-17hammer to
  use %%{_libdir}
- Added XFree86-libs as BuildRequires (because of tkinter)
- Fixed duplicate listing of plat-linux2
- Fixed exclusion of lib-dynload/japanese
- Added lib64 patch for the japanese codecs
- Use setup magic instead of using tar directly on JapaneseCodecs

* Tue Nov  5 2002 Mihai Ibanescu <misa@redhat.com>
2.2.2-2
- Fix #76912 (python-tools contains idle, which uses tkinter, but there is no
  requirement of tkinter from python-tools).
- Fix #74013 (rpm is missing the /usr/lib/python2.2/test directory)

* Mon Nov  4 2002 Mihai Ibanescu <misa@redhat.com>
- builds as python2 require a different libdb
- changed the buildroot name of python to match python2 builds

* Fri Nov  1 2002 Mihai Ibanescu <misa@redhat.com>
- updated python to 2.2.2 and adjusted the patches accordingly

* Mon Oct 21 2002 Mihai Ibanescu <misa@redhat.com>
- Fix #53930 (Python-2.2.1-buildroot-bytecode.patch)
- Added BuildPrereq dependency on gcc-c++

* Fri Aug 30 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-17
- security fix for _execvpe

* Tue Aug 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-16
- Fix  #71011,#71134, #58157

* Wed Aug  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-15
- Resurrect tkinter
- Fix for distutils (#67671)
- Fix #69962

* Thu Jul 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-14
- Obsolete tkinter/tkinter2 (#69838)

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-13
- Doc fixes (#53951) - not on alpha at the momemt

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-12
- fix pydoc (#68082)

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-11
- Add db4-devel as a BuildPrereq

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.2.1-10
- automated rebuild

* Mon Jun 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-9
- Add Japanese codecs (#66352)

* Tue Jun 11 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-8
- No more tkinter...

* Wed May 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-7
- Rebuild

* Tue May 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-6
- Add the email subcomponent (#65301)

* Fri May 10 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-5
- Rebuild

* Thu May 02 2002 Than Ngo <than@redhat.com> 2.2.1-4
- rebuild i new enviroment

* Tue Apr 23 2002 Trond Eivind Glomsrød <teg@redhat.com>
- Use ucs2, not ucs4, to avoid breaking tkinter (#63965)

* Mon Apr 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-2
- Make it use db4

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1-1
- 2.2.1 - a bugfix-only release

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-16
- the same, but in builddirs - this will remove them from the 
  docs package, which doesn't look in the buildroot for files.

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-15
- Get rid of temporary files and .cvsignores included 
  in the tarball and make install

* Fri Apr  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-14
- Don't own lib-tk in main package, only in tkinter (#62753)

* Mon Mar 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-13
- rebuild

* Mon Mar 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-12
- rebuild

* Fri Mar  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-11
- Add a not to the Distutils obsoletes test (doh!)

* Fri Mar  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-10
- Rebuild

* Mon Feb 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-9
- Only obsolete Distutils when built as python

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-8
- Make files in /usr/bin install side by side with python 1.5 when
- Drop explicit requirement of db4
  built as python2

* Thu Jan 31 2002 Elliot Lee <sopwith@redhat.com> 2.2-7
- Use version and pybasever macros to make updating easy
- Use _smp_mflags macro

* Tue Jan 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-6
- Add db4-devel to BuildPrereq

* Fri Jan 25 2002 Nalin Dahyabhai <nalin@redhat.com> 2.2-5
- disable ndbm support, which is db2 in disguise (really interesting things
  can happen when you mix db2 and db4 in a single application)

* Thu Jan 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-4
- Obsolete subpackages if necesarry 
- provide versioned python2
- build with db4

* Wed Jan 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2-3
- Alpha toolchain broken. Disable build on alpha.
- New openssl

* Wed Dec 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-1
- 2.2 final

* Fri Dec 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.11c1
- 2.2 RC 1
- Don't include the _tkinter module in the main package - it's 
  already in the tkiter packace
- Turn off the mpzmodule, something broke in the buildroot

* Wed Nov 28 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.10b2
- Use -fPIC for OPT as well, in lack of a proper libpython.so

* Mon Nov 26 2001 Matt Wilson <msw@redhat.com> 2.2-0.9b2
- changed DESTDIR to point to / so that distutils will install dynload
  modules properly in the installroot

* Fri Nov 16 2001 Matt Wilson <msw@redhat.com> 2.2-0.8b2
- 2.2b2

* Fri Oct 26 2001 Matt Wilson <msw@redhat.com> 2.2-0.7b1
- python2ify

* Fri Oct 19 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.5b1
- 2.2b1

* Sun Sep 30 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.4a4
- 2.2a4
- Enable UCS4 support
- Enable IPv6
- Provide distutils
- Include msgfmt.py and pygettext.py

* Fri Sep 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.3a3
- Obsolete Distutils, which is now part of the main package
- Obsolete python2

* Thu Sep 13 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.2a3
- Add docs, tools and tkinter subpackages, to match the 1.5 layout

* Wed Sep 12 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2-0.1a3
- 2.2a3
- don't build tix and blt extensions

* Mon Aug 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add tk and tix to build dependencies

* Sat Jul 21 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.1 bugfix release - with a GPL compatible license

* Fri Jul 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add new build dependencies (#49753)

* Tue Jun 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- build with -fPIC

* Fri Jun  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1
- reorganization of file includes

* Wed Dec 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix the "requires" clause, it lacked a space causing problems
- use %%{_tmppath}
- don't define name, version etc
- add the available patches from the Python home page

* Fri Dec 15 2000 Matt Wilson <msw@redhat.com>
- added devel subpackage

* Fri Dec 15 2000 Matt Wilson <msw@redhat.com>
- modify all files to use "python2.0" as the intrepter
- don't build the Expat bindings
- build against db1

* Mon Oct 16 2000 Jeremy Hylton <jeremy@beopen.com>
- updated for 2.0 final

* Mon Oct  9 2000 Jeremy Hylton <jeremy@beopen.com>
- updated for 2.0c1
- build audioop, imageop, and rgbimg extension modules
- include xml.parsers subpackage
- add test.xml.out to files list

* Thu Oct  5 2000 Jeremy Hylton <jeremy@beopen.com>
- added bin/python2.0 to files list (suggested by Martin v. L?)

* Tue Sep 26 2000 Jeremy Hylton <jeremy@beopen.com>
- updated for release 1 of 2.0b2
- use .bz2 version of Python source

* Tue Sep 12 2000 Jeremy Hylton <jeremy@beopen.com>
- Version 2 of 2.0b1
- Make the package relocatable.  Thanks to Suchandra Thapa.
- Exclude Tkinter from main RPM.  If it is in a separate RPM, it is
  easier to track Tk releases.
