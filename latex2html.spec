%define compactversion	2002-2-1
%define latex2htmldir %{_prefix}/lib/%{name}

Summary:	LaTeX to HTML converter
Name:		latex2html
Version:	2012
Release:	11
License:	GPLv2+
Group:		Publishing
Url:		http://www.latex2html.org
Source0:	http://mirrors.ctan.org/support/latex2html/%{name}-%{version}.tgz
Patch0:		%{name}-2002-gsfonts.patch
Patch1:		%{name}-%{compactversion}-path.patch
Patch2:		%{name}-perlversion.patch
Patch3:		%{name}-doc-address.patch
Patch4:		%{name}-pdfoutput.patch
Patch5:		%{name}-gs-stderr.patch
Patch6:		%{name}-perlcall.patch
Patch7:		%{name}-htmladdimg.patch
BuildArch:	noarch
BuildRequires:	perl(L2hos)
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	texlive-latex-bin
BuildRequires:	ghostscript
BuildRequires:	ghostscript-dvipdf
BuildRequires:	netpbm
Requires:	ghostscript >= 6.50
Requires:	giftrans
Requires:	netpbm
Requires:	perl >= 5.004
Requires:	tetex-latex >= 1.0.7
Requires:	tetex-dvips >= 1.0.7
Requires:	texlive-latex-bin

%description
Elaborate perl program to convert latex documents to html, using LaTeX
to process images and equations.  

%prep
%setup -q 
%apply_patches

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
sed -i -e 's#/usr/local/bin/perl#%{__perl}#' %{buildroot}%{_prefix}/lib/latex2html/cweb2html/cweb2html
sed -i -e 's#/usr/local/bin/perl#%{__perl}#' %{buildroot}%{_prefix}/lib/latex2html/makeseg/makeseg
sed -i -e 's#/usr/local/bin/perl#%{__perl}#' %{buildroot}%{latex2htmldir}/makemap


# fix some installation path
sed -i -e "s#%{_builddir}/%{name}-%{compactversion}#%{latex2htmldir}#" \
	%{buildroot}%{latex2htmldir}/cfgcache.pm
sed -i -e "s#%{_datadir}/lib/latex2html#%{latex2htmldir}#" \
	%{buildroot}%{latex2htmldir}/cfgcache.pm

# these files are already included in tetex
(cd %{buildroot}%{_datadir}/texmf/tex/latex/html
rm -f floatflt.ins latin9.def url.sty
)

#(cd docs 
#rm -f changebar.sty url.sty
#TEXINPUTS=.:../texinputs:
#export TEXINPUTS
#latex manual
#latex manual
#latex manual
#dvipdf manual.dvi
#install -m 644 manual.pdf %{buildroot}%{_defaultdocdir}/%{name}-%{version})

%post
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%files
%{_bindir}/*
%dir %{latex2htmldir}
%{latex2htmldir}/*
%{_datadir}/texmf/tex/latex/html/
%{_docdir}/%{name}-%{version}

