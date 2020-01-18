Name:           perl-CPANPLUS-Dist-Build
Version:        0.70
Release:        2%{?dist}
Summary:        Module::Build extension for CPANPLUS
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CPANPLUS-Dist-Build/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/CPANPLUS-Dist-Build-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
%if %{defined perl_bootstrap}
BuildRequires:  perl(base)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.59
BuildRequires:  perl(ExtUtils::MM_Unix)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
%else
BuildRequires:  perl(inc::Module::Install)
%if !(0%{?rhel} >= 7)
BuildRequires:  perl(Module::Install::AutoLicense)
%endif
# Module::Install::GithubMeta is optional and not usefull
%endif
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
# This is a plug-in for CPANPLUS, specify reverse dependency here
BuildRequires:  perl(CPANPLUS) >= 0.84
BuildRequires:  perl(CPANPLUS::Error)
BuildRequires:  perl(CPANPLUS::Internals::Constants)
BuildRequires:  perl(Cwd)
%if 0%(perl -e 'print $] > 5.017')
BuildRequires:  perl(deprecate)
%endif
BuildRequires:  perl(Exporter)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(if)
BuildRequires:  perl(IPC::Cmd) >= 0.42
BuildRequires:  perl(Locale::Maketext::Simple)
BuildRequires:  perl(Module::Build) >= 0.32
BuildRequires:  perl(Module::Load::Conditional) >= 0.30
BuildRequires:  perl(Params::Check) >= 0.26
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(CPANPLUS::Configure)
BuildRequires:  perl(CPANPLUS::Backend)
BuildRequires:  perl(CPANPLUS::Internals::Utils)
BuildRequires:  perl(CPANPLUS::Module::Author::Fake)
BuildRequires:  perl(CPANPLUS::Module::Fake)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::Installed)
BuildRequires:  perl(ExtUtils::Packlist)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Build::ConfigData)
BuildRequires:  perl(Test::More) >= 0.47
# Optional tests:
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# This is a plug-in for CPANPLUS, specify reverse dependency here
Requires:       perl(CPANPLUS) >= 0.84
%if 0%(perl -e 'print $] > 5.017')
Requires:       perl(deprecate)
%endif
Requires:       perl(Exporter)
Requires:       perl(IPC::Cmd) >= 0.42
Requires:       perl(Module::Build) >= 0.32
Requires:       perl(Module::Load::Conditional) >= 0.30
Requires:       perl(Params::Check) >= 0.26

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((IPC::Cmd|Module::Load::Conditional|Params::Check)\\)$

%description
CPANPLUS::Dist::Build is a distribution class for Module::Build related
modules. With this package, you can create, install and uninstall
Module::Build-based perl modules by calling CPANPLUS::Dist methods.

%prep
%setup -q -n CPANPLUS-Dist-Build-%{version}
%if !%{defined perl_bootstrap}
# Remove bundled modules only if non-core modules are available becuase this
# is a core module.
rm -r ./inc/*
sed -i -e '/^\/inc\//d' MANIFEST
%if 0%{?rhel} >= 7
sed -i -e '/^auto_license\s/d' Makefile.PL
%endif
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Jun 17 2013 Petr Pisar <ppisar@redhat.com> - 0.70-2
- Do not build-require Module::Install::AutoLicense on RHEL >= 7

* Mon Jun 10 2013 Petr Pisar <ppisar@redhat.com> 0.70-1
- Specfile autogenerated by cpanspec 1.78.
