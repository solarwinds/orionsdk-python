# emulate mock bubblewrap dependency; delete with proper source
%if %{?rhel:0}%{!?rhel:1}
%global rhel	%(rpm -qf --qf "%{version}" /etc/issue)
%endif
%if %{?dist:0}%{!?dist:1}
%global dist	el%{?rhel}%{!?rhel:0}
%endif

# Actually, don't strip at all since we are not even building debug packages
%define __strip /bin/true
%global debug_package	%{nil}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?fedora}
%global with_python3 1
%endif

%global	modname	orionsdk
%global	branch	master

Summary:	Python client for interacting with the SolarWinds Orion API
Name:		python-%{modname}

%global URL	https://pypi.org/project/orionsdk/

Source0:	%{URL}/archive/%{branch}.tar.gz
%define pp_ver	%(tar xzOf %{S:0} %{modname}-python-%{branch}/%{modname}/__init__.py | awk -F'"' '/^__version__/{print $2}')

Version:	%{pp_ver}
Release:	0.1
Epoch:		0

License:	APL2; Josh Clark / Solarwinds
packager:	Bishop Clark <bishopolis@gmail.com>
Group:		Development/Libraries
URL:		%{URL}

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	python-requests
BuildRequires:	python-six

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-requests
BuildRequires: python3-six
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires: python-unittest2
BuildRequires: python-argparse
Requires: python-argparse
BuildRequires: python-backports-ssl_match_hostname
Requires: python-backports-ssl_match_hostname
%endif

Requires: python-six

%global	aptnoarch noarch
%global	aptnodist nodist
%global	noadddist nodist
#global	noaddevr  noevr

%description
%{Summary}


%prep
%setup -q -n %{modname}-python-%{branch}


%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%{__python2} setup.py build

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}

# remove tests that got installed into the buildroot
rm -rf %{buildroot}/%{python3_sitelib}/tests/

# Remove executable bit from installed files.
find %{buildroot}/%{python3_sitelib} -type f -exec chmod -x {} \;
popd
%endif

%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

# remove tests that got installed into the buildroot
rm -rf %{buildroot}/%{python2_sitelib}/tests/

rm -rf %{buildroot}/%{python2_sitelib}/%{modname}-%{version}*egg-info

# Remove executable bit from installed files.
find %{buildroot}/%{python2_sitelib} -type f -exec chmod -x {} \;


%check
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd

%endif

#%%{__python2} setup.py test

%clean
[ "%{buildroot}" = "/" ] || [ ! -d %{buildroot} ] || rm -rf %{buildroot}


%files
%doc LICENSE README.md requirements.txt samples %{modname}.egg-info
%{python2_sitelib}/%{modname}/


%changelog
* %(date +"%a %b %d %Y") $Author: build $ %{version}-%{release}

  $Log$
