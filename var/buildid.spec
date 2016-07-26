%include SPECS/.buildid.rpmmacro

Name:		buildid
Version:	%{version_formatted_short}
Release:	%{timestamp}.%{?dist}
Summary:	Gathers information about a code build for reuse by packaging and deployment
BuildArch:	noarch

Group:		Applications/System
License:	GPLv2
URL:		http://github.com/jamesread/buildid
Source0:	buildid.zip

BuildRequires:	zip
Requires:	python python-lxml

%description
buildid

%prep
%setup -q -n buildid-%{version_formatted_short}-%{tag}

%post
ln -sf /usr/lib/buildid/app.py /usr/sbin/buildid

%postun
rm -f /usr/sbin/buildid

%build
mkdir -p "%{buildroot}/usr/lib/buildid/"
cp app/* "%{buildroot}/usr/lib/buildid/"

mkdir -p "%{buildroot}/usr/share/doc/buildid/"
cp README.md "%{buildroot}/usr/share/doc/buildid/"

mkdir -p "%{buildroot}/usr/share/man/man1/"
cp doc/buildid.1.gz "%{buildroot}/usr/share/man/man1/"

%files
/usr/lib/buildid/
%doc /usr/share/doc/buildid/README.md
%doc /usr/share/man/man1/buildid.1.gz

%changelog
* Wed Aug 12 2015 James Read <contact@jwread.com> 1.0.0-1
	Version 1.0.0-1
