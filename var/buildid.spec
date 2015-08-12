Name:		buildid
Version:	1.0.0
Release:	1%{?dist}
Summary:	Gathers information about a code build for reuse by packaging and deployment
BuildArch:	noarch

Group:		Applications/System
License:	GPLv2
URL:		http://github.com/jamesread/buildid
Source0:	buildid.zip

BuildRequires:	zip
Requires:	python

%description
buildid

%prep
%setup -q

%build
mkdir -p %{buildroot}/usr/sbin/
cp buildid %{buildroot}/usr/sbin/

mkdir -p %{buildroot}/usr/share/doc/buildid/
cp README.md %{buildroot}/usr/share/doc/buildid/

mkdir -p %{buildroot}/usr/share/man/man1/
cp doc/buildid.1.gz %{buildroot}/usr/share/man/man1/

%files
/usr/sbin/buildid
%doc /usr/share/doc/buildid/README.md
%doc /usr/share/man/man1/buildid.1.gz

%changelog
* Wed Aug 12 2015 James Read <contact@jwread.com> 1.0.0-1
	Version 1.0.0-1