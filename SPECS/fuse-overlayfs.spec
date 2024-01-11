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
Patch0: fuse-overlayfs-openat2-unsupported.patch
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
- Resolves: #2185132

* Fri Dec 02 2022 Jindrich Novy <jnovy@redhat.com> - 1.10-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.10
- Related: #2123641

* Fri Jun 10 2022 Jindrich Novy <jnovy@redhat.com> - 1.9-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.9
- Related: #2061390

* Wed May 11 2022 Jindrich Novy <jnovy@redhat.com> - 1.8.2-2
- BuildRequires: /usr/bin/go-md2man
- Related: #2061390

* Wed Feb 02 2022 Jindrich Novy <jnovy@redhat.com> - 1.8.2-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.8.2
- Related: #2001445

* Wed Jan 19 2022 Jindrich Novy <jnovy@redhat.com> - 1.8.1-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.8.1
- Related: #2001445

* Wed Dec 22 2021 Jindrich Novy <jnovy@redhat.com> - 1.8-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.8
- Related: #2001445

* Wed Aug 11 2021 Jindrich Novy <jnovy@redhat.com> - 1.7.1-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.7.1
- Related: #1934415

* Thu Jul 29 2021 Jindrich Novy <jnovy@redhat.com> - 1.7-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.7
- Related: #1934415

* Wed Jun 23 2021 Jindrich Novy <jnovy@redhat.com> - 1.6-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.6
- Related: #1934415

* Thu Mar 25 2021 Jindrich Novy <jnovy@redhat.com> - 1.5.0-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.5.0
- Related: #1934415

* Fri Jan 29 2021 Jindrich Novy <jnovy@redhat.com> - 1.4.0-2
- disable openat2 syscall again - still unsupported in current RHEL8 kernel
- Related: #1883490

* Sat Jan 23 2021 Jindrich Novy <jnovy@redhat.com> - 1.4.0-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.4.0
- Related: #1883490

* Thu Nov 26 2020 Jindrich Novy <jnovy@redhat.com> - 1.3.0-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.3.0
- Related: #1883490

* Mon Nov 09 2020 Jindrich Novy <jnovy@redhat.com> - 1.2.0-3
- be sure to harden the linked binary
- Related: #1883490

* Thu Oct 29 2020 Jindrich Novy <jnovy@redhat.com> - 1.2.0-2
- ensure fuse module is loaded
- Related: #1883490

* Wed Oct 21 2020 Jindrich Novy <jnovy@redhat.com> - 1.2.0-1
- synchronize with stream-container-tools-rhel8
- Related: #1883490

* Fri Sep 18 2020 Jindrich Novy <jnovy@redhat.com> - 1.1.2-3
- fix "error bind mounting /dev from host into mount namespace"
  (the openat2 syscall is not yet supported by the RHEL8 kernel)
- Resolves: #1867447

* Tue Aug 11 2020 Jindrich Novy <jnovy@redhat.com> - 1.1.2-2
- use proper CFLAGS
- Related: #1821193

* Mon Jun 29 2020 Jindrich Novy <jnovy@redhat.com> - 1.1.2-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.1.2
- Related: #1821193

* Mon Jun 22 2020 Jindrich Novy <jnovy@redhat.com> - 1.1.1-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.1.1
- Related: #1821193

* Thu Jun 18 2020 Jindrich Novy <jnovy@redhat.com> - 1.1.0-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v1.1.0
- Related: #1821193

* Tue May 12 2020 Jindrich Novy <jnovy@redhat.com> - 1.0.0-1
- synchronize containter-tools 8.3.0 with 8.2.1
- Related: #1821193

* Tue Apr 07 2020 Jindrich Novy <jnovy@redhat.com> - 0.7.8-1
- update to https://github.com/containers/fuse-overlayfs/releases/tag/v0.7.8
- Related: #1821193

* Thu Mar 19 2020 Jindrich Novy <jnovy@redhat.com> - 0.7.2-5
- latest iteration of segfault fix patch, thanks to Giuseppe Scrivano
- Resolves: #1805017

* Fri Mar 06 2020 Jindrich Novy <jnovy@redhat.com> - 0.7.2-4
- replace "fuse-overlayfs segfault" patch with improved one
  due to application to a different context
- Resolves: #1805017

* Thu Feb 20 2020 Jindrich Novy <jnovy@redhat.com> - 0.7.2-3
- fix "fuse-overlayfs segfault"
- Resolves: #1805017

* Mon Feb 17 2020 Jindrich Novy <jnovy@redhat.com> - 0.7.2-2
- fix "useradd and groupadd fail under rootless Buildah and podman"
- Resolves: #1803496

* Fri Nov 29 2019 Jindrich Novy <jnovy@redhat.com> - 0.7.2-1
- update to 0.7.2
- Related: RHELPLAN-25139

* Fri Nov 29 2019 Jindrich Novy <jnovy@redhat.com> - 0.7.1-1
- update to 0.7.1
- Related: RHELPLAN-25139

* Mon Nov 18 2019 Jindrich Novy <jnovy@redhat.com> - 0.7-1
- update to 0.7
- apply patch to fix build on RHEL-8
- Related: RHELPLAN-25139

* Sat Jun 15 2019 Lokesh Mandvekar <lsm5@redhat.com> - 0.4.1-1
- Resolves: #1720654 - rebase to v0.4.1

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
