Name:           xcp-ng-xapi-storage
Version:        1.1.0
Release:        1%{?dist}
Summary:        XCP-ng implementation of the xapi-storage interface
License:        LGPLv2.1
URL:            https://github.com/xcp-ng/xcp-ng-xapi-storage
Source0:        https://github.com/xcp-ng/xcp-ng-xapi-storage/archive/v%{version}/%{name}-%{version}.tar.gz

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
