%define compactversion	2002-2-1

Name: 		latex2html
Summary: 	LaTeX to HTML converter
Version: 	2012
Release: 	1
License: 	GPLv2+
Group: 		Publishing
URL: 		http://www.latex2html.org
Source: 	http://mirrors.ctan.org/support/latex2html/%{name}-%{version}.tgz
Patch0:		%{name}-2002-gsfonts.patch
Patch1:		%{name}-%{compactversion}-path.patch
Patch2:		%{name}-perlversion.patch
Patch3:		%{name}-doc-address.patch
Patch4:		%{name}-pdfoutput.patch
Patch5:		%{name}-gs-stderr.patch
Patch6:		%{name}-perlcall.patch
Patch7:		%{name}-htmladdimg.patch
Requires:	ghostscript >= 6.50
Requires:	giftrans
Requires:	netpbm
Requires:	perl >= 5.004
Requires: 	tetex-latex >= 1.0.7
Requires:	tetex-dvips >= 1.0.7
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex ghostscript
BuildRequires:	ghostscript-dvipdf
BuildRequires:	netpbm
BuildArchitectures:	noarch

%define latex2htmldir %{_prefix}/lib/%{name}

%description
Elaborate perl program to convert latex documents to html, using LaTeX
to process images and equations.  

%prep
%setup -q 
%patch0 -p1 -b .gsfonts
%patch1 -p1
%patch2 -p1 -b .perl
%patch3 -p1 -b .address
%patch4 -p1
%patch5 -p1 -b .stderr
%patch6 -p1 
%patch7 -p1

%build
TMP=/var/tmp ./configure \
	--with-gs=%{_bindir}/gs \
	--with-texpath=%{_datadir}/texmf/tex/ \
	--without-mktexlsr \
	--with-perl=%{__perl} \
	--prefix=%{_prefix} \
	--shlibdir=%{latex2htmldir} \
	--with-initex="%{_bindir}/tex -ini" \
	--with-rgb=/usr/share/X11/rgb.txt
%make

%install
rm -rf %{buildroot}
# custom "make install" so paths are proper in the perl programs

mkdir -p %{buildroot}%{_bindir} \
	%{buildroot}%{latex2htmldir}

install -m 755 latex2html %{buildroot}%{_bindir}
install -m 755 pstoimg %{buildroot}%{_bindir}
install -m 755 texexpand %{buildroot}%{_bindir}

rm -f L2hos/Win32.pm
rm -f L2hos/Dos.pm
rm -f L2hos/Mac.pm
rm -f L2hos/OS2.pm

cp -avRf IndicTeX-HTML %{buildroot}%{latex2htmldir}/
cp -avRf L2hos.pm %{buildroot}%{latex2htmldir}/
cp -avRf L2hos %{buildroot}%{latex2htmldir}/
cp -avRf XyMTeX-HTML %{buildroot}%{latex2htmldir}/
cp -avRf cweb2html %{buildroot}%{latex2htmldir}/
cp -avRf docs %{buildroot}%{latex2htmldir}/
cp -avRf example %{buildroot}%{latex2htmldir}/
cp -avRf foilhtml %{buildroot}%{latex2htmldir}/
cp -avRf icons %{buildroot}%{latex2htmldir}/
cp -avRf makeseg %{buildroot}%{latex2htmldir}/
cp -avRf styles %{buildroot}%{latex2htmldir}/
cp -avRf texinputs %{buildroot}%{latex2htmldir}/
cp -avRf versions %{buildroot}%{latex2htmldir}/

cp -avRf cfgcache.pm dot.latex2html-init l2hconf.pm makemap readme.hthtml \
	%{buildroot}%{latex2htmldir}/

mkdir -p %{buildroot}%{_datadir}/texmf/tex/latex/html
cp -avRf texinputs/* %{buildroot}%{_datadir}/texmf/tex/latex/html

mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -avRf Changes FAQ MANIFEST README readme.hthtml TODO BUGS INSTALL \
	dot.latex2html-init example \
		%{buildroot}%{_defaultdocdir}/%{name}-%{version}

# fix perl path in a few places:
perl -pi -e 's#/usr/local/bin/perl#%{__perl}#' %{buildroot}%{_prefix}/lib/latex2html/cweb2html/cweb2html
perl -pi -e 's#/usr/local/bin/perl#%{__perl}#' %{buildroot}%{_prefix}/lib/latex2html/makeseg/makeseg
perl -pi -e 's#/usr/local/bin/perl#%{__perl}#' %{buildroot}%{latex2htmldir}/makemap


# fix some installation path
perl -pi -e "s#%{_builddir}/%{name}-%{compactversion}#%{latex2htmldir}#" \
	%{buildroot}%{latex2htmldir}/cfgcache.pm
perl -pi -e "s#%{_datadir}/lib/latex2html#%{latex2htmldir}#" \
	%{buildroot}%{latex2htmldir}/cfgcache.pm

# these files are already included in tetex
(cd %{buildroot}%{_datadir}/texmf/tex/latex/html
rm -f floatflt.ins latin9.def url.sty
)

(cd docs 
rm -f changebar.sty url.sty
TEXINPUTS=.:../texinputs:
export TEXINPUTS
latex manual
latex manual
latex manual
dvipdf manual.dvi
install -m 644 manual.pdf %{buildroot}%{_defaultdocdir}/%{name}-%{version})

%clean
rm -rf %{buildroot}

%post
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%files
%defattr(-,root,root,0755)
%{_bindir}/*
%dir %{latex2htmldir}
%{latex2htmldir}/*
%{_datadir}/texmf/tex/latex/html/
%{_docdir}/%{name}-%{version}




%changelog
* Mon Mar 26 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2008-6
+ Revision: 787037
- Add BuildRequires: netpbm to make sure PNG+GIF support is detected

* Mon Mar 26 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2008-5
+ Revision: 787022
- Fix compatibility with perl 5.14
- Remove some unneeded files
- Fix build with current rpm
- Clean up spec file

* Sun May 15 2011 Oden Eriksson <oeriksson@mandriva.com> 2008-4
+ Revision: 674845
- fix deps
- mass rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 2008-3mdv2011.0
+ Revision: 520138
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2008-2mdv2010.0
+ Revision: 425501
- rebuild

* Mon Dec 29 2008 Emmanuel Andry <eandry@mandriva.org> 2008-1mdv2009.1
+ Revision: 321225
- New version 2008
- fix old X11 path in configure options
- fix license

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 2002-13mdv2009.0
+ Revision: 136535
- restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 2002-13mdv2008.1
+ Revision: 128338
- kill re-definition of %%buildroot on Pixel's request


* Thu Mar 01 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 2002-13mdv2007.0
+ Revision: 130671
- Use %%mkrel.
- Import latex2html

* Sat Mar 19 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2002-12mdk
- Added Patch7, for html.sty from latex2html author.

* Sat Mar 12 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2002-11mdk
- latex2html-2002-2-1 (25-Oct-2004).
- removed \\address{...} usage in documentation (Patch3).
- Let latex/pdflatex checking in html.sty more robust (Patch4).
- Added Patch5 because 'gs -h' outputs to stderr.

* Sat Aug 28 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2002-10mdk
- Rebuilt.

