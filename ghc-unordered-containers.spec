#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	unordered-containers
Summary:	Efficient hashing-based container types
Summary(pl.UTF-8):	Typy wydajnych kontenerów opartych na haszowaniu
Name:		ghc-%{pkgname}
Version:	0.2.10.0
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/unordered-containers
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	5994101f6b1f19b264dcfdf863f57324
Patch0:		hashable-1.3.patch
URL:		http://hackage.haskell.org/package/unordered-containers
BuildRequires:	ghc >= 7.8.1
BuildRequires:	ghc-base >= 4.7
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-deepseq >= 1.1
BuildRequires:	ghc-hashable >= 1.0.1.1
%if %{with prof}
BuildRequires:	ghc-prof >= 7.8.1
BuildRequires:	ghc-base-prof >= 4.7
BuildRequires:	ghc-deepseq-prof >= 1.1
BuildRequires:	ghc-hashable-prof >= 1.0.1.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.7
Requires:	ghc-deepseq >= 1.1
Requires:	ghc-hashable >= 1.0.1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Efficient hashing-based container types. The containers have been
optimized for performance critical use, both in terms of large data
quantities and high speed.

%description -l pl.UTF-8
Typy wydajnych kontenerów opartych na haszowaniu. Kontenery zostały
zoptymalizowane pod kątem zastosowań krytycznych wydajnościowo,
zarówno pod względem dużych ilości danych, jak i dużej szybkości.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.7
Requires:	ghc-deepseq-prof >= 1.1
Requires:	ghc-hashable-prof >= 1.0.1.1

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for %{pkgname} ghc package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname} ghc package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch -P0 -p1

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSunordered-containers-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSunordered-containers-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSunordered-containers-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashMap
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashMap/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashMap/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashMap/Strict
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashMap/Strict/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashMap/Strict/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashSet
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashSet/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashSet/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSunordered-containers-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashMap/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashMap/Strict/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/HashSet/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
