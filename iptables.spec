Name: iptables
Summary: Tools for managing Linux kernel packet filtering capabilities
Version: 1.4.12.2
Release: 1
Source0: http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
Source1: iptables-config
Patch0: iptables-1.4.11-cloexec.patch
Group: System/Base
URL: http://www.netfilter.org/
License: GPLv2
BuildRequires: kernel-headers
Conflicts: kernel < 2.4.20

%description
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.

%package ipv6
Summary: IPv6 support for iptables
Group: System/Base
Requires: %{name} = %{version}-%{release}

%description ipv6
The iptables package contains IPv6 (the next version of the IP
protocol) support for iptables. Iptables controls the Linux kernel
network packet filtering code, allowing you to set up firewalls and IP
masquerading. 

Install iptables-ipv6 if you need to set up firewalling for your
network and you are using ipv6.

%package devel
Summary: Development package for iptables
Group: System/Base
Requires: %{name} = %{version}-%{release}

%description devel
iptables development headers and libraries.

The iptc interface is upstream marked as not public. The interface is not 
stable and may change with every new version. It is therefore unsupported.

%prep
%setup -q
%patch0 -p1 -b .cloexec

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
./configure --enable-devel --enable-libipq --bindir=/bin --sbindir=/sbin --sysconfdir=/etc --libdir=/%{_lib} --libexecdir=/%{_lib} --mandir=%{_mandir} --includedir=%{_includedir} --with-kernel=/usr --with-kbuild=/usr --with-ksource=/usr

# do not use rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} 
# remove la file(s)
rm -f %{buildroot}/%{_lib}/*.la

# install ip*tables.h header files
install -m 644 include/ip*tables.h %{buildroot}%{_includedir}/
install -d -m 755 %{buildroot}%{_includedir}/iptables
install -m 644 include/iptables/internal.h %{buildroot}%{_includedir}/iptables/

# install ipulog header file
install -d -m 755 %{buildroot}%{_includedir}/libipulog/
install -m 644 include/libipulog/*.h %{buildroot}%{_includedir}/libipulog/

# create symlinks for devel so libs
install -d -m 755 %{buildroot}%{_libdir}
for i in %{buildroot}/%{_lib}/*.so; do
    ln -s ../../%{_lib}/${i##*/} %{buildroot}%{_libdir}/${i##*/}
done

# move pkgconfig to %{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}/%{_libdir}/

# install init scripts and configuration files
install -d -m 755 %{buildroot}/etc/sysconfig
install -c -m 755 %{SOURCE1} %{buildroot}/etc/sysconfig/iptables-config
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE1} > ip6tables-config
install -c -m 755 ip6tables-config %{buildroot}/etc/sysconfig/ip6tables-config

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING INSTALL INCOMPATIBILITIES
%config(noreplace) %attr(0600,root,root) /etc/sysconfig/iptables-config
/sbin/iptables*
/sbin/xtables-multi
/bin/iptables-xml
%{_mandir}/man1/iptables*
%{_mandir}/man8/iptables*
%dir /%{_lib}/xtables
/%{_lib}/xtables/libipt*
/%{_lib}/xtables/libxt*
/%{_lib}/libip*tc.so.*
/%{_lib}/libipq.so.*
/%{_lib}/libxtables.so.*

%files ipv6
%defattr(-,root,root)
%config(noreplace) %attr(0600,root,root) /etc/sysconfig/ip6tables-config
/sbin/ip6tables*
%{_mandir}/man8/ip6tables*
/%{_lib}/xtables/libip6t*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/iptables
%{_includedir}/iptables/*.h
%{_includedir}/*.h
%dir %{_includedir}/libiptc
%{_includedir}/libiptc/*.h
%dir %{_includedir}/libipulog
%{_includedir}/libipulog/*.h
%{_mandir}/man3/*
/%{_lib}/libip*tc.so
/%{_lib}/libipq.so
/%{_lib}/libxtables.so
%{_libdir}/libip*tc.so
%{_libdir}/libipq.so
%{_libdir}/libxtables.so
%{_libdir}/pkgconfig/libipq.pc
%{_libdir}/pkgconfig/libiptc.pc
%{_libdir}/pkgconfig/libip4tc.pc
%{_libdir}/pkgconfig/libip6tc.pc
%{_libdir}/pkgconfig/xtables.pc
