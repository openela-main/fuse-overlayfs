%global git0 https://github.com/containers/%{name}

%{!?_modulesloaddir:%global _modulesloaddir %{_usr}/lib/modules-load.d}

Name: fuse-overlayfs
Version: 1.11
Release: 1%{?dist}
Summary: FUSE overlay+shiftfs implementation for rootless containers
License: GPLv3+
URL: %{git0}
ExclusiveArch: aarch64 %{arm} ppc64le s390x x86_64
Source0: %{git0}/archive/v%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: fuse3-devel
BuildRequires: gcc
BuildRequires: git
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
* Tue Apr 11 2023 Jindrich Novy <jnovy@redhat.com> - 1.11-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.11
- Resolves: #2185133

* Tue Feb 07 2023 Jindrich Novy <jnovy@redhat.com> - 1.10-2
- rebuild
- Resolves: #2130975

* Fri Dec 02 2022 Jindrich Novy <jnovy@redhat.com> - 1.10-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.10
- Related: #2124478

* Fri Jun 10 2022 Jindrich Novy <jnovy@redhat.com> - 1.9-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.9
- Related: #2061316

* Wed May 11 2022 Jindrich Novy <jnovy@redhat.com> - 1.8.2-2
- BuildRequires: /usr/bin/go-md2man
- Related: #2061316

* Wed Feb 02 2022 Jindrich Novy <jnovy@redhat.com> - 1.8.2-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.8.2
- Related: #2000051

* Wed Jan 19 2022 Jindrich Novy <jnovy@redhat.com> - 1.8.1-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.8.1
- Related: #2000051

* Wed Dec 22 2021 Jindrich Novy <jnovy@redhat.com> - 1.8-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.8
- Related: #2000051

* Fri Oct 01 2021 Jindrich Novy <jnovy@redhat.com> - 1.7.1-3
- perform only sanity/installability tests for now
- Related: #2000051

* Wed Sep 29 2021 Jindrich Novy <jnovy@redhat.com> - 1.7.1-2
- add gating.yaml
- Related: #2000051

* Fri Sep 03 2021 Jindrich Novy <jnovy@redhat.com> - 1.7.1-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.7.1
- Related: #2000051

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.7-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Jul 29 2021 Jindrich Novy <jnovy@redhat.com> - 1.7-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.7
- Related: #1970747

* Wed Jun 23 2021 Jindrich Novy <jnovy@redhat.com> - 1.6-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.6
- Related: #1970747

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 1.5.0-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Thu Mar 25 2021 Jindrich Novy <jnovy@redhat.com> - 1.5.0-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.5.0

* Tue Jan 26 2021 Jindrich Novy <jnovy@redhat.com> - 1.4.0-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.4.0

* Thu Nov 26 2020 Jindrich Novy <jnovy@redhat.com> - 1.3.0-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.3.0

* Mon Nov 09 2020 Jindrich Novy <jnovy@redhat.com> - 1.2.0-4
- be sure to harden the linked binary

* Thu Oct 29 2020 Jindrich Novy <jnovy@redhat.com> - 1.2.0-3
- ensure fuse module is loaded

* Fri Oct 09 2020 Jindrich Novy <jnovy@redhat.com> - 1.2.0-2
- use 1.2.0 tarball from the release, not tag

* Fri Oct 09 2020 Jindrich Novy <jnovy@redhat.com> - 1.2.0-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.2.0

* Thu Sep 17 2020 Jindrich Novy <jnovy@redhat.com> - 1.1.2-2
- sync with rhel8-8.3.0

* Thu Sep 17 2020 Jindrich Novy <jnovy@redhat.com> - 1.1.2-1
- use proper CFLAGS
- Related: #1821193

* Sat Jun 15 2019 Lokesh Mandvekar <lsm5@redhat.com> - 0.4.1-1
- Resolves: #1720654 - rebase to v0.4.1

* Wed Feb 20 2019 Frantisek Kluknavsky <fkluknav@redhat.com> - 0.3-4.dev.gitd760789
- rebase

* Wed Jan 16 2019 Frantisek Kluknavsky <fkluknav@redhat.com> - 0.3-2
- rebase
- Resolves:#1666510

* Wed Oct 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-7.dev.git50c7a50
- Resolves: #1640232
- built commit 50c7a50

* Fri Aug 10 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-6.dev.git1c72a1a
- Resolves: #1614856 - add manpage
- built commit 1c72a1a
- add BR: go-md2man

* Fri Aug 10 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-5.dev.gitd40ac75
- built commit d40ac75
- remove fedora bz ids
- Exclude ix86 and ppc64

* Mon Jul 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-4.dev.git79c70fd
- Resolves: #1609598 - initial upload to Fedora
- bundled gnulib

* Mon Jul 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-3.dev.git79c70fd
- correct license field

* Mon Jul 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-2.dev.git79c70fd
- fix license

* Sun Jul 29 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-1.dev.git13575b6
- First package for Fedora
