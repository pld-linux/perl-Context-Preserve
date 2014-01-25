#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Context
%define		pnam	Preserve
%include	/usr/lib/rpm/macros.perl
Summary:	Context::Preserve - run code after a subroutine call, preserving the context the subroutine would have seen if it were the last statement in the caller
#Summary(pl.UTF-8):	
Name:		perl-Context-Preserve
Version:	0.01
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/J/JR/JROCKWAY/Context-Preserve-0.01.tar.gz
# Source0-md5:	e28c24d9e85d3f7de1c7b9a545ba991a
URL:		http://search.cpan.org/dist/Context-Preserve/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Test-Exception
BuildRequires:	perl-Test-use-ok
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sometimes you need to call a function, get the results, act on the
results, then return the result of the function.  This is painful
because of contexts; the original function can behave different if
it's called in void, scalar, or list context.  You can ignore the
various cases and just pick one, but that's fragile.  To do things
right, you need to see which case you're being called in, and then
call the function in that context.  This results in 3 code paths,
which is a pain to type in (and maintain).

This module automates the process.  You provide a coderef that is the
"original function", and another coderef to run after the original
runs.  You can modify the return value (aliased to @_) here, and do
whatever else you need to do.  wantarray is correct inside both
coderefs; in "after", though, the return value is ignored and the
value wantarray returns is related to the context that the original
function was called in.

# %description -l pl.UTF-8
# TODO

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%dir %{perl_vendorlib}/Context
%{perl_vendorlib}/Context/Preserve.pm
%{_mandir}/man3/*
