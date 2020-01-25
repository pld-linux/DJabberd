#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define	pdir	DJabberd
Summary:	DJabberd - scalable, extensible Jabber/XMPP server
Summary(pl.UTF-8):	DJabberd - skalowalny, rozszerzalny serwer Jabbera/XMPP
Name:		DJabberd
Version:	0.83
Release:	0.4
# same as perl 
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/B/BR/BRADFITZ/%{pdir}-%{version}.tar.gz
# Source0-md5:	ce449b6ef429eb65ec03be4c8d19b1aa
Source1:	djabberd.conf
Source2:	djabberd-log.conf
URL:		http://search.cpan.org/dist/DJabberd/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Danga-Socke) >= 1.51
BuildRequires:	perl(Digest::HMAC_SHA1)
BuildRequires:	perl-Log-Log4perl
BuildRequires:	perl-Net-DNS >= 0.48
BuildRequires:	perl-Net-SSLeay
BuildRequires:	perl-XML-LibXML-SAX
BuildRequires:	perl-XML-SAX
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# this is mentioned in example component
%define		_noautoreq	'perl(DJabberd::Bot::Eliza)'

%description
DJabberd was the answer to LiveJournal's Jabber (XMPP) server needs.
It's a Jabber server where almost everything defers to hooks to be
implemented by plugins. It does the core spec itself (including SSL,
StartTLS, server-to-server, etc), but it doesn't come with any way to
do authentication or storage or rosters, etc. You'll need to go pick
up a plugin to do those.

%description -l pl.UTF-8
DJabberd to odpowiedź na potrzeby odnośnie serwera Jabbera (XMPP) dla
serwisu LiveJournal. Jest to serwer Jabbera, w którym prawie wszystko
jest przekazywane do uchwytów implementowanych przez wtyczki. Sam
serwer wykonuje podstawowe zadania (wraz z SSL, StartTLS, komunikacją
serwer-serwer), ale nie zawiera niczego do uwierzytelniania,
przechowywania danych czy rosterów - do wszystkiego trzeba dodać
wtyczkę.

%prep
%setup -q -n %{pdir}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/djabberd
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/djabberd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/djabberd/log.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES
%attr(755,root,root) %{_bindir}/djabberd
%{perl_vendorlib}/DJabberd.pm
%{perl_vendorlib}/DJabberd
%dir %{_sysconfdir}/djabberd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/djabberd/djabberd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/djabberd/log.conf
%{_mandir}/man3/*
