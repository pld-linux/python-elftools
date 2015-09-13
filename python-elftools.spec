#
# TODO:
#	- check why the tests fail
#
# Conditional build:
%bcond_with	tests	# run tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	elftools
Summary:	Pure-Python library for parsing and analyzing ELF files
Summary(pl.UTF-8):	Czysto pythonowa biblioteka do analizy plików ELF
Name:		python-%{module}
Version:	0.23
Release:	2
License:	public domain
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/p/pyelftools/pyelftools-%{version}.tar.gz
# Source0-md5:	aa7cefa8bd2f63d7b017440c9084f310
URL:		https://github.com/eliben/pyelftools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
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

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2

%if %{with tests}
%{__python} ./test/all_tests.py
%endif
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}

%if %{with tests}
%{__python3} ./test/all_tests.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
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
