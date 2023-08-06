Name: libfsext
Version: 20220829
Release: 1
Summary: Library to support the Extended File System (ext) format
Group: System Environment/Libraries
License: LGPLv3+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfsext
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
              
BuildRequires: gcc              

%description -n libfsext
Library to support the Extended File System (ext) format

%package -n libfsext-static
Summary: Library to support the Extended File System (ext) format
Group: Development/Libraries
Requires: libfsext = %{version}-%{release}

%description -n libfsext-static
Static library version of libfsext.

%package -n libfsext-devel
Summary: Header files and libraries for developing applications for libfsext
Group: Development/Libraries
Requires: libfsext = %{version}-%{release}

%description -n libfsext-devel
Header files and libraries for developing applications for libfsext.

%package -n libfsext-python3
Summary: Python 3 bindings for libfsext
Group: System Environment/Libraries
Requires: libfsext = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libfsext-python3
Python 3 bindings for libfsext

%package -n libfsext-tools
Summary: Several tools for reading Extended File System (ext) volumes
Group: Applications/System
Requires: libfsext = %{version}-%{release} openssl fuse-libs 
BuildRequires: openssl-devel fuse-devel 

%description -n libfsext-tools
Several tools for reading Extended File System (ext) volumes

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libfsext
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libfsext-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libfsext-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfsext.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfsext-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libfsext-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Aug 30 2022 Joachim Metz <joachim.metz@gmail.com> 20220829-1
- Auto-generated

