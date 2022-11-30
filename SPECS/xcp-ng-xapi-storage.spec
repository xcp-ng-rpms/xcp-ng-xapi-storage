Name:           xcp-ng-xapi-storage
Version:        1.0.2
Release:        3.0.0.runx.2%{?dist}
Summary:        XCP-ng implementation of the xapi-storage interface
License:        LGPLv2.1
URL:            https://github.com/xcp-ng/xcp-ng-xapi-storage
Source0:        https://github.com/xcp-ng/xcp-ng-xapi-storage/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0: 0001-feat-plugins-add-a-new-raw-device-plugin-5.patch
Patch1: 0002-fix-qemudisk-connect-must-raise-only-after-N-attempt.patch
Patch2: 0003-fix-raw-device-plugin-does-not-follow-device-symlink.patch
Patch3: 0004-fix-qemuback-use-communicate-method-to-wait-process-.patch
Patch4: 0005-feat-qemudisk-use-blkio-and-cpu-cgroups.patch
Patch5: 0006-feat-nbdclient-use-a-block-size-of-4096bytes-to-incr.patch
Patch6: 0007-feat-nbdclient-ensure-we-use-a-none-scheduler-passth.patch
Patch7: 0008-feat-callbacks-add-a-trash-folder-to-destroy-volumes.patch
Patch8: 0009-feat-coalesce-kill-task-after-5s-in-stop_task.patch
Patch9: 0010-chore-README.md-fix-dependencies-to-install-destinat.patch
Patch10: 0011-feat-datapath-provide-a-new-Fspdisk-plugin-to-suppor.patch
Patch11: 0012-feat-fsp-plugin-implement-vdi-creation-by-relying-on.patch

BuildRequires:  cmake3
BuildRequires:  make
BuildRequires:  python-setuptools

Requires:       nbd
Requires:       python-psutil
Requires:       qemu-dp
Requires:       systemd
Requires:       xapi-storage

%description
XCP-ng implementation of the xapi-storage interface.

%prep
%autosetup -p1

%build
mkdir build
cd build
%cmake3 ..
make

%install
cd build
%make_install

%post
%systemd_post qemuback.service

%preun
%systemd_preun qemuback.service

%postun
%systemd_postun_with_restart qemuback.service

%files
%license LICENSE README.md
%{_bindir}/qemuback.py
%{_docdir}/xcp-ng-xapi-storage/
%{_libexecdir}/xapi-storage-script/
%{_prefix}/lib/python2.7/site-packages/xapi/storage/libs/
%{_prefix}/lib/python2.7/site-packages/xcp_ng_xapi_storage_libs-*-py2.7.egg-info
%{_prefix}/lib/systemd/system/qemuback.service

%changelog
* Wed Nov 30 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.0.2-3.0.0.runx.2
- Add 0012-feat-fsp-plugin-implement-vdi-creation-by-relying-on.patch

* Thu Aug 12 2021 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.0.2-3.0.0.runx.1
- Add 0011-feat-datapath-provide-a-new-Fspdisk-plugin-to-suppor.patch

* Wed Jul 01 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.2-3
- Rebuild for XCP-ng 8.2

* Fri Dec 20 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.2-2
- Rebuild for XCP-ng 8.1

* Wed Sep 11 2019 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.0.2-1
- Initial package
