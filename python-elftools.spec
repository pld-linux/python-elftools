#
# Conditional build:
%bcond_with	tests	# run tests (require some specific version of binutils)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	elftools
Summary:	Pure-Python library for parsing and analyzing ELF files
Summary(pl.UTF-8):	Czysto pythonowa biblioteka do analizy plików ELF
Name:		python-%{module}
Version:	0.29
Release:	3
License:	public domain
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/p/pyelftools/pyelftools-%{version}.tar.gz
# Source0-md5:	2afc97cd239c0dea0cca97d00d3dcb42
URL:		https://github.com/eliben/pyelftools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif
%if %{with tests}
# readelf
BuildRequires:	binutils
# llvm-dwarfdump
BuildRequires:	llvm
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pyelftools is a pure-Python library for parsing and analyzing ELF
files and DWARF debugging information.

%description -l pl.UTF-8
pyelftools to czysto pythonowa biblioteka do analizy plików ELF oraz
informacji dla debuggera DWARF.

%package -n python3-%{module}
Summary:	Pure-Python library for parsing and analyzing ELF files
Summary(pl.UTF-8):	Czysto pythonowa biblioteka do analizy plików ELF
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
pyelftools is a pure-Python library for parsing and analyzing ELF
files and DWARF debugging information.

%description -n python3-%{module} -l pl.UTF-8
pyelftools to czysto pythonowa biblioteka do analizy plików ELF oraz
informacji dla debuggera DWARF.

%prep
%setup -q -n pyelftools-%{version}

# prebuilt x86_64 binaries
%{__rm} test/external_tools/{readelf,llvm-dwarfdump}
%if %{with tests}
ln -sf /usr/bin/readelf test/external_tools/readelf
ln -sf /usr/bin/llvm-dwarfdump test/external_tools/llvm-dwarfdump
%endif

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} ./test/all_tests.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} ./test/all_tests.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

# readelf clone example
%{__rm} $RPM_BUILD_ROOT%{_bindir}/readelf.py

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE CHANGES
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/pyelftools-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE CHANGES
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/pyelftools-%{version}-py*.egg-info
%endif
