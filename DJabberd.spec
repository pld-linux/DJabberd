#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	DJabberd
Summary:	DJabberd - scalable, extensible Jabber/XMPP server.
#Summary(pl):	
Name:		DJabberd
Version:	0.83
Release:	0.4
# same as perl 
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{version}.tar.gz
Source1:	djabberd.conf
Source2:	djabberd-log.conf
# Source0-md5:	ce449b6ef429eb65ec03be4c8d19b1aa
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(Danga::Socket) >= 1.51
BuildRequires:	perl(Digest::HMAC_SHA1)
BuildRequires:	perl(Log::Log4perl)
BuildRequires:	perl(Net::DNS) >= 0.48
BuildRequires:	perl(Net::SSLeay)
BuildRequires:	perl(XML::LibXML::SAX)
BuildRequires:	perl(XML::SAX)
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# this is mentioned in example component
%define		_noautoreq	'perl(DJabberd::Bot::Eliza)'

%description
DJabberd was the answer to LiveJournal's Jabber (XMPP)
server needs.  We needed:

Basically we wanted the swiss army knife of Jabber servers (think
qpsmtpd or mod_perl), but none existed in any language.  While some
popular Jabber servers let us do pluggable auth, none let us get our
hands into roster storage, vcards, avatars, presence, etc.

So we made DJabberd.  It's a Jabber server where almost everything
defers to hooks to be implemented by plugins.  It does the core spec
itself (including SSL, StartTLS, server-to-server, etc), but it
doesn't come with any way to do authentication or storage or rosters,
etc.  You'll need to go pick up a plugin to do those.

You should be able to plop DJabberd into your existing systems /
userbase with minimal pain.  Just find a plugin that's close (if a
perfect match doesn't already exist!) and tweak.

DJabberd is event-based so we can have really low per-connection
memory requirements, smaller than is possible with a threaded jabber
server.  Because of this, all plugins can operate asynchronously,
taking as long as they want to finish their work, or to decline to the
next handler.  (in the meantime, while plugins wait on a response from
whatever they're talking to, the DJabberd event loop continues at full
speed) However, that's more work, so some plugins may choose to
operate synchronously, but they do so with the understanding that
those plugins will cause the whole server to get bogged down.  If
you're running a Jabber server for 5 users, you may not care that the
SQLite authentication backend pauses your server for milliseconds at a
time, but on a site with hundreds of thousands of connections, that
wouldn't be acceptable.  Watch out for those plugins.



# %description -l pl
# TODO

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
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/djabberd/
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/djabberd/log.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES
%{perl_vendorlib}/DJabberd.pm
%{perl_vendorlib}/DJabberd/
%{_mandir}/man3/*
%attr(755,root,root) %{_bindir}/djabberd
%dir %{_sysconfdir}/djabberd
%config %{_sysconfdir}/djabberd/djabberd.conf
%config %{_sysconfdir}/djabberd/log.conf
