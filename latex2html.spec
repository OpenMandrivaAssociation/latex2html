%define name	latex2html
%define version	2008
%define rel 2
%define compactversion	2002-2-1

Name: 		%{name}
Summary: 	LaTeX to HTML converter
Version: 	%{version}
Release: 	%mkrel %{rel}
License: 	GPLv2+
Group: 		Publishing
URL: 		http://www.latex2html.org
Source: 	http://saftsack.fs.uni-bayreuth.de/~latex2ht/current/%{name}-%{version}.tar.gz
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
BuildRoot:	%{_tmppath}/ltx-%{version}-root
BuildArchitectures:	noarch
%define _requires_exceptions Win32

%define graphic_format	png	# use "gif" or "png"
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
rm -rf $RPM_BUILD_ROOT
# custom "make install" so paths are proper in the perl programs

mkdir -p $RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{latex2htmldir}

install -m 755 latex2html $RPM_BUILD_ROOT%{_bindir}
install -m 755 pstoimg $RPM_BUILD_ROOT%{_bindir}
install -m 755 texexpand $RPM_BUILD_ROOT%{_bindir}

cp -avRf IndicTeX-HTML $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf L2hos.pm $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf L2hos $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf XyMTeX-HTML $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf cweb2html $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf docs $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf example $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf foilhtml $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf icons $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf makeseg $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf styles $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf texinputs $RPM_BUILD_ROOT%{latex2htmldir}/
cp -avRf versions $RPM_BUILD_ROOT%{latex2htmldir}/

cp -avRf cfgcache.pm dot.latex2html-init l2hconf.pm makemap readme.hthtml \
	$RPM_BUILD_ROOT%{latex2htmldir}/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/html
cp -avRf texinputs/* $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/html

mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp -avRf Changes FAQ MANIFEST README readme.hthtml TODO BUGS INSTALL \
	dot.latex2html-init example \
		$RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

# fix perl path in a few places:
perl -pi -e 's#/usr/local/bin/perl#%{__perl}#' $RPM_BUILD_ROOT%{_prefix}/lib/latex2html/cweb2html/cweb2html
perl -pi -e 's#/usr/local/bin/perl#%{__perl}#' $RPM_BUILD_ROOT%{_prefix}/lib/latex2html/makeseg/makeseg
perl -pi -e 's#/usr/local/bin/perl#%{__perl}#' $RPM_BUILD_ROOT%{latex2htmldir}/makemap

# fix some installation path
perl -pi -e "s#$RPM_BUILD_DIR/%{name}-%{compactversion}#%{latex2htmldir}#" \
	$RPM_BUILD_ROOT%{latex2htmldir}/cfgcache.pm
perl -pi -e "s#%{_datadir}/lib/latex2html#%{latex2htmldir}#" \
	$RPM_BUILD_ROOT%{latex2htmldir}/cfgcache.pm

# these files are already included in tetex
(cd $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/html
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
install -m 644 manual.pdf $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version})

%clean
rm -rf $RPM_BUILD_ROOT

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


