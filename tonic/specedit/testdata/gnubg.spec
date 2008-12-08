###############################################################
#
# Spec file for package gnubg (Version 0.14).
#
# Copyright (c) 2003 Achim Mueller, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# please send bugfixes or comments to info@gnubg.org
#
###############################################################

Name:         gnubg-backgammonbase-edition
License:      GNU General Public License (GPL) - all versions
Group:        Amusements/Games/Board/Other
Packager:     <bgnori@gmail.com>
Summary:      A backgammon game and analyser for backgammonbase.com
Version:      0.2
Release:      1 
Source:       %{name}-%{version}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
URL:          http://backgammonbase.com


%description
GNU Backgammon (@gnubg{}) is software for playing and analysing backgammon
positions, games and matches. It's based on a neural network. Although it
already plays at a very high level, it's still work in progress. You may
play GNU Backgammon using the command line or a graphical interface


Original GNU Backgammon Authors:
--------
Joseph Heled <joseph@gnubg.org>
Oystein Johansen <oystein@gnubg.org>
David Montgomery
Jim Segrave
Joern Thyssen <jth@gnubg.org>
Gary Wong <gtw@gnu.org>



%package databases
Summary:     Databases for gnubg
Requires:    %{name}
Group:        Amusements/Games/Board/Other

%description databases
This package contains the GNU Backgammon bearoff databases.

%package sounds
Summary:     Sounds for gnubg
Requires:    %{name}
Group:        Amusements/Games/Board/Other

%description sounds
This package contains the sounds for GNU Backgammon.

%define prefix /usr


%prep
%setup

%build
./autogen.sh
./configure --prefix=%{prefix} \
	          --infodir=${RPM_BUILD_ROOT}%{prefix}/share/info \
	          --mandir=${RPM_BUILD_ROOT}%{prefix}/share/man \
            --datadir=${RPM_BUILD_ROOT}%{prefix}/share \
            --without-board3d \
            --with-gtk \
            --with-python \
            --with-readline \
            --enable-sse=yes \
            --without-sound \
            --enable-threads
make  

%install
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;
mkdir -p $RPM_BUILD_ROOT%{prefix}
make prefix=$RPM_BUILD_ROOT%{prefix} install-strip

# create this dir empty so we can own it
mkdir -p $RPM_BUILD_ROOT%{_datadir}/aclocal
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
 
%post
/sbin/install-info %{_infodir}/gnubg.info.gz %{_infodir}/dir
 
%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gnubg.info.gz %{_infodir}/dir
fi

%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
#%doc AUTHORS README COPYING ChangeLog
%{prefix}/bin/*
#%{prefix}/share/info/*
%{prefix}/share/gnubg/met/*
# Match Equity Tables.

#%{prefix}/share/gnubg/*.png
%{prefix}/share/gnubg/boards.xml
%{prefix}/share/gnubg/gnubg.gtkrc
%{prefix}/share/gnubg/gnubg.wd
%{prefix}/share/gnubg/gnubg.weights
%{prefix}/share/gnubg/gnubg.sql
%{prefix}/share/gnubg/scripts/*.pyc
%{prefix}/share/gnubg/scripts/*.pyo
%{prefix}/share/gnubg/scripts/*.py
%{prefix}/share/gnubg/flags/*.png
%{prefix}/share/gnubg/pixmaps/gnubg-big.png
%{prefix}/share/gnubg/scripts/query_player.sh
%{prefix}/share/icons/hicolor/16x16/apps/gnubg.png
%{prefix}/share/icons/hicolor/22x22/apps/gnubg.png
%{prefix}/share/icons/hicolor/24x24/apps/gnubg.png
%{prefix}/share/icons/hicolor/32x32/apps/gnubg.png
%{prefix}/share/icons/hicolor/48x48/apps/gnubg.png
#flag images resource selection

%{prefix}/share/gnubg/fonts/*
#fonts.

#%{prefix}/share/gnubg/texinfo.dtd
#no such item

%{prefix}/share/gnubg/textures*
%{prefix}/share/locale/*/*/*
#%{prefix}/share/man/*/*

%files databases
%{prefix}/share/gnubg/*.bd

%files sounds
%{prefix}/share/gnubg/sounds/*


%changelog -n gnubg
* Sat Nov 18 2006 - <ace@gnubg.org>
- some slight changes in specfile

* Wed Dec 28 2004 - <ace@gnubg.org>
- new weights including pruning

* Mon Oct 11 2004 - <ace@gnubg.org>
- fixed some minor bugs

* Wed Sep 01 2004 - <ace@gnubg.org>
- new rpms with 3d enabled

* Wed Nov 05 2003 - <ace@gnubg.org>
- made the spec suit to redhat and suse <ace@gnubg.org>
- disabled 3d (still problems with nvidia)
- added gpg signature

* Thu Oct 23 2003 - <ace@gnubg.org>
- disabled gdbm and guile
- changed info- and manpath

* Mon Oct 20 2003 - <ace@gnubg.org>
- divided into three packages (gnubg, databases, sounds)

* Fri Oct 18 2003 - <ace@gnubg.org>
- initial package (Version 0.14)
