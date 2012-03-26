%define compactversion	2002-2-1

Name: 		latex2html
Summary: 	LaTeX to HTML converter
Version: 	2008
Release: 	6
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
Patch8:		latex2html-2008-perl-5.14.patch
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
%patch8 -p1 -b .p514~

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

# remove stuff we don't need (but that fills up the harddisk
# and adds dependencies anyway)
rm -f	%buildroot%_prefix/lib/latex2html/L2hos/Win32.pm \
	%buildroot%_prefix/lib/latex2html/L2hos/DOS.pm \
	%buildroot%_prefix/lib/latex2html/L2hos/Mac.pm \
	%buildroot%_prefix/lib/latex2html/L2hos/OS2.pm

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


