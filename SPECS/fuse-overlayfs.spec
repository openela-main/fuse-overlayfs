%global git0 https://github.com/containers/%{name}

%{!?_modulesloaddir:%global _modulesloaddir %{_usr}/lib/modules-load.d}

Name: fuse-overlayfs
Version: 1.14
Release: 2%{?dist}
Summary: FUSE overlay+shiftfs implementation for rootless containers
License: GPLv3+
URL: %{git0}
ExclusiveArch: aarch64 %{arm} ppc64le s390x x86_64
Source0: %{git0}/archive/v%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: fuse3-devel
BuildRequires: gcc
BuildRequires: git-core
BuildRequires: /usr/bin/go-md2man
BuildRequires: make
Requires: kmod
Requires: fuse3

%description
%{summary}.

%package devel
Summary: %{summary}
BuildArch: noarch

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%prep
%autosetup -Sgit

%build
export CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
./autogen.sh
./configure --prefix=%{_usr} --libdir=%{_libdir}
%{__make} generate-man

%install
make DESTDIR=%{buildroot} install install-man
install -d %{buildroot}%{_modulesloaddir}
echo fuse > %{buildroot}%{_modulesloaddir}/fuse-overlayfs.conf

%post
modprobe fuse > /dev/null 2>&1 || :

%check

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_modulesloaddir}/fuse-overlayfs.conf

%changelog
* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 1.14-2
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Mon Jul 15 2024 Jindrich Novy <jnovy@redhat.com> - 1.14-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.14
- Related: RHEL-39410
