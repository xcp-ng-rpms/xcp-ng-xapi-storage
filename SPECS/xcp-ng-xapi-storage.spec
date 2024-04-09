Name:           xcp-ng-xapi-storage
Version:        1.2.0
Release:        2%{?dist}
Summary:        XCP-ng implementation of the xapi-storage interface
License:        LGPLv2.1
URL:            https://github.com/xcp-ng/xcp-ng-xapi-storage
Source0:        https://github.com/xcp-ng/xcp-ng-xapi-storage/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires:  cmake3
BuildRequires:  make
BuildRequires:  python-setuptools

%description
XCP-ng implementation of the xapi-storage interface.

%package        libs
Summary:        XCP-ng implementation of SMAPIv3 storage-scripts libraries
Requires:       xapi-storage
Requires:       nbd
Requires:       python2-psutil
Conflicts:      xcp-ng-xapi-storage

%description    libs
Common python code for various SMAPIv3 Datapath and Volume plugins.

%package        datapath-tapdisk
Summary:        XCP-ng implementation of tapdisk SMAPIv3 Datapath plugin
Requires:       xcp-ng-xapi-storage-libs
Requires:       blktap
Conflicts:      xcp-ng-xapi-storage

%description    datapath-tapdisk
SMAPIv3 Datapath plugins using tapdisk

#%%package        datapath-qemudisk
#Summary:        XCP-ng implementation of qcow2 SMAPIv3 Datapath plugin
#Requires:       python-psutil
#Requires:       qemu-dp
#Requires:       systemd

%package        volume-zfsvol
Summary:        XCP-ng implementation of ZFS SMAPIv3 Volume plugin
Requires:       xcp-ng-xapi-storage-libs
Requires:       xcp-ng-xapi-storage-datapath-tapdisk
Requires:       zfs >= 2.1

%description    volume-zfsvol
SMAPIv3 Volume plugins storing each VDI in a ZFS volume.

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

#%%post
#%%systemd_post qemuback.service
#
#%%preun
#%%systemd_preun qemuback.service
#
#%%postun
#%%systemd_postun_with_restart qemuback.service

%files libs
%license LICENSE README.md
%{_docdir}/xcp-ng-xapi-storage/
%{_prefix}/lib/python2.7/site-packages/xapi/storage/libs/
%{_prefix}/lib/python2.7/site-packages/xcp_ng_xapi_storage_libs-*-py2.7.egg-info

%files datapath-tapdisk
%{_libexecdir}/xapi-storage-script/datapath/tapdisk

#%%files datapath-qemudisk
#%%{_libexecdir}/xapi-storage-script/datapath/qemudisk
#%%{_bindir}/qemuback.py
#%%{_prefix}/lib/systemd/system/qemuback.service

%files volume-zfsvol
%{_libexecdir}/xapi-storage-script/volume/org.xen.xapi.storage.zfs-vol

%changelog
* Tue Apr 09 2024 Guillaume Thouvenin <guillaume.thouvenin@vates.tech> - 1.2.0-2
- Add missing dependency to python2-psutil

* Thu Apr 04 2024 Yann Dirson <yann.dirson@vates.tech> - 1.2.0-1
- Include new zfs-vol volume plugin
- Change package to noarch
- Stop shipping qemudisk datapath plugins, qemuback daemon, and other volume plugins
- Split RPM between libs and individual datapath and volume plugins

* Fri Jan 13 2023 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.1.0-1
- Add a new RAW device plugin
- Add a trash folder to destroy volumes during coalesce
- Few NBD changes to increase performance (block size, none scheduler, ...)

* Wed Nov 30 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.2-4
- Rebuild for XCP-ng 8.3

* Wed Jul 01 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.2-3
- Rebuild for XCP-ng 8.2

* Fri Dec 20 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.2-2
- Rebuild for XCP-ng 8.1

* Wed Sep 11 2019 Ronan Abhamon <ronan.abhamon@vates.fr> - 1.0.2-1
- Initial package
