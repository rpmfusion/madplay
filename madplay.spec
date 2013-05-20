Name:          madplay
Version:       0.15.2b
Release:       9%{?dist}
Summary:       MPEG audio decoder and player

Group:         Applications/Multimedia
License:       GPLv2+
URL:           http://www.underbit.com/products/mad/
Source0:       http://download.sourceforge.net/mad/%{name}-%{version}.tar.gz
Source1:       mp3license
Patch0:        %{name}-0.15.2b-abxtest-tempfile.patch
Patch1:        http://ftp.debian.org/debian/pool/main/m/madplay/madplay_0.15.2b-4.diff.gz
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:      %{_sbindir}/update-alternatives
BuildRequires: libmad-devel
BuildRequires: libid3tag-devel
#BuildRequires: esound-devel
BuildRequires: gettext
%{?_with_alsa:BuildRequires: alsa-lib-devel}
Provides:      mp3-cmdline
Provides:      mad = %{version}-%{release}
Obsoletes:     mad < %{version}-%{release}

%description
madplay is a command-line MPEG audio decoder and player based on the
MAD library (libmad).  For details about MAD, see the separately
distributed libmad package.


%prep
%setup -q
%patch0
%patch1 -p1
%{__patch} -i debian/patches/00_ucs4.diff
sed -i -e 's/[-lz]/[]/' configure.ac ; sed -i -e 's/ -lz / /' configure
touch -r aclocal.m4 configure.ac
# Recode CREDITS to utf-8
/usr/bin/iconv -f iso8859-1 -t utf-8 CREDITS > CREDITS.conv \
    && /bin/mv CREDITS.conv CREDITS


%build
%configure %{?_with_alsa} --disable-dependency-tracking
make %{?_smp_mflags}
make %{?_smp_mflags} madtime # madmix mad123 madtag # sometime, when they work


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -pm 755 madtime $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE1} .
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_sbindir}/update-alternatives --install %{_bindir}/mp3-cmdline \
  mp3-cmdline %{_bindir}/madplay 30


%postun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove mp3-cmdline %{_bindir}/madplay
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{_bindir}/abxtest
%{_bindir}/madplay
%{_bindir}/madtime
%{_mandir}/man1/abxtest.1*
%{_mandir}/man1/madplay.1*


%changelog
* Mon May 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.15.2b-9
- Disable esound

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.15.2b-8
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.15.2b-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.15.2b-6
- rebuild for new F11 features

* Wed Sep 24 2008 David Timms <iinet.net.au@dtimms> 0.15.2b-5
- import and bump release for rpmfusion.
- update license to GPLv2+ to meet Fedora guidelines.
- change Group to Applications/Multimedia
- convert CREDITS to utf-8

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.15.2b-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.15.2b-3
- Rebuild.

* Mon May  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.15.2b-2
- Fix insecure temp file usage in abxtest (patch from SuSE).
- Fix display of non-ASCII tags in UTF-8 setups (patch from Debian).

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Nov  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.15.2b-0.lvn.1
- Avoid spurious zlib build dependency.
- Make Obsoletes versioned.
- Build with dependency tracking disabled.
- Drop zero Epochs.

* Sat Jun  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.15.2-0.lvn.1.b
- Update to 0.15.2b.
- Add "--with alsa" flag to build with ALSA support, not done by default yet.

* Wed Feb 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.15.1-0.lvn.1.b
- Update to 0.15.1b.
- Include madtime in package.

* Mon Jun 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.15.0-0.fdr.1.b
- Update to 0.15.0b.
- Split separate from the old mad package to follow upstream.
- Rename to madplay, provide and obsolete mad.

* Thu Apr 24 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.14.2-0.fdr.3.b
- Fix missing "main" package dependencies in *-devel.
- Include patch from Debian, possibly fixes #187 comment 7, and adds
  pkgconfig files for libraries.

* Sun Apr 20 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.14.2-0.fdr.2.b
- Split into mad, libmad, -devel, libid3tag and -devel packages (#187).
- Provide mp3-cmdline virtual package and alternative.
- Build shared library.

* Fri Apr  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.14.2-0.fdr.1.b
- Update to current Fedora guidelines.
- Exclude %%{_libdir}/*.la.

* Thu Feb 20 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.14.2b-1.fedora.1
- First Fedora release, based on Matthias Saou's work.

* Fri Sep 27 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuild for Red Hat Linux 8.0 (missing because of license issues).
- Spec file cleanup.

* Tue Mar 12 2002 Bill Nottingham <notting@redhat.com> 0.14.2b-3
- ship libid3tag too

* Thu Feb 21 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Mon Jan 28 2002 Bill Nottingham <notting@redhat.com>
- split libmad off into a separate package
