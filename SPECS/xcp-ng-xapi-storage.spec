Name:           xcp-ng-xapi-storage
Version:        1.2.1
Release:        1%{?dist}
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
Requires:       xapi-storage-script
Requires:       nbd
Conflicts:      xcp-ng-xapi-storage

%description    libs
Common python code for various SMAPIv3 Datapath and Volume plugins.

%package        datapath-tapdisk
Summary:        XCP-ng implementation of tapdisk SMAPIv3 Datapath plugin
Requires:       xcp-ng-xapi-storage-libs
Requires:       blktap
Conflicts:      xcp-ng-xapi-storage

%description    datapath-tapdisk
SMAPIv3 Datapath plugin using tapdisk

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
SMAPIv3 Volume plugin storing each VDI in a ZFS volume.

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

# qemuback has been disabled because currently it is not working and it needs
# to be fixed. When fixed we will renable it.
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
# Don't install qcow2util.py and qemudisk.py because qcow2 is not yet supported
%exclude %{_prefix}/lib/python2.7/site-packages/xapi/storage/libs/libcow/qcow2util.py
%exclude %{_prefix}/lib/python2.7/site-packages/xapi/storage/libs/qemudisk.py

%files datapath-tapdisk
%{_libexecdir}/xapi-storage-script/datapath/tapdisk

#%%files datapath-qemudisk
#%%{_libexecdir}/xapi-storage-script/datapath/qemudisk
#%%{_bindir}/qemuback.py
#%%{_prefix}/lib/systemd/system/qemuback.service

%files volume-zfsvol
%{_libexecdir}/xapi-storage-script/volume/org.xen.xapi.storage.zfs-vol

%changelog
* Tue Jun 18 2024 Guillaume Thouvenin <guillaume.thouvenin@vates.tech> - 1.2.1-1
- Don't install qcow2util.py and qemudisk.py because qcow2 is not yet supported
- Remove dependency to python2-psutil that was required by qcow2

* Tue Apr 16 2024 Guillaume Thouvenin <guillaume.thouvenin@vates.tech> - 1.2.0-3
- Add missing dependency to xapi-storage-script
- Minor fixes in datapath and volume description
- Add a comment regarding disabling qemuback.service

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
