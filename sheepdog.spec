# TODO:
# - more clusters support:
#   - zookeeper (--enable-zookeeper) [http://zookeeper.apache.org/, -lzookeeper_mt, zookeeper.h]
#   - shepherd (--enable-shepherd)
# - http request service (--enable-http, BR: curl-devel, fcgi-devel)?
# - nfs server service (--enable-nfs, BR: libtirpc-devel)?
# - diskvnodes (--enable-diskvnodes)?
# - earthquake debugger (--enable-earthquake)?
# - lttng tracing (--enable-lttng-ust, BR: lttng-ust-devel)?
# - accelio  (--enable-accelio, BR: accelio-devel)
# - PLDify and register init script
Summary:	Sheepdog - distributed storage system for QEMU/KVM
Summary(pl.UTF-8):	Sheepdog - rozproszony system przechowywania danych dla QEMU/KVM
Name:		sheepdog
Version:	1.0.1
Release:	1
License:	GPL v2
Group:		Applications/System
#Source0Download: https://github.com/sheepdog/sheepdog/tags
Source0:	https://github.com/collie/sheepdog/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0f7f865ceefc07a88dfec5c2f1912e32
Patch0:		%{name}-no-common.patch
URL:		http://www.osrg.net/sheepdog/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	corosync-devel >= 2
BuildRequires:	groff
BuildRequires:	libfuse-devel >= 2.8.0
BuildRequires:	libqb-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	userspace-rcu-devel >= 0.6.0
%ifarch %{x8664}
BuildRequires:	yasm >= 1.2.0
%endif
Requires:	libfuse >= 2.8.0
Requires:	userspace-rcu >= 0.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sheepdog is a distributed storage system for QEMU/KVM. It provides
highly available block level storage volumes that can be attached to
QEMU/KVM virtual machines. Sheepdog scales to several hundreds nodes,
and supports advanced volume management features such as snapshot,
cloning, and thin provisioning.

%description -l pl.UTF-8
Sheepdog to rozproszony system przechowywania danych dla QEMU/KVM.
Udostępnia na poziomie urządzeń blokowych wolumeny o wysokiej
dostępności, które można podłączyć do maszyn wirtualnych QEMU/KVM.
Sheepdog skaluje się do setek węzłów i obsługuje zaawansowane
możliwości zarządzania wolumentami, takie jak migawka (snapshot),
klonowanie i nadalokacja (thin provisioning).

%package -n bash-completion-%{name}
Summary:        bash-completion for dog command
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla polecenia dog
Group:          Applications/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
BuildArch:	noarch

%description -n bash-completion-%{name}
bash-completion for sheepdog dog command.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe dopełnianie składni dla polecenia dog z pakietu sheepdog.

%package libs
Summary:	sheepdog shared library
Summary(pl.UTF-8):	Biblioteka współdzielona sheepdog
Group:		Libraries

%description libs
sheepdog shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona sheepdog.

%package devel
Summary:	Header files for sheepdog library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sheepdog
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for sheepdog library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sheepdog.

%package static
Summary:	Static sheepdog library
Summary(pl.UTF-8):	Biblioteka statyczna sheepdog
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static sheepdog library.

%description static -l pl.UTF-8
Biblioteka statyczna sheepdog.

%prep
%setup -q
%patch0 -p1

%ifarch x32
# currently not supported in lib/isa-l, but let's check
%{__sed} -i -e 's/-f elf64/-f elfx32/' \
	configure.ac \
	lib/isa-l/make.inc
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-systemd \
	--with-initddir=/etc/rc.d/init.d \
	--with-systemdsystemunitdir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsheepdog.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README INSTALL
%attr(755,root,root) %{_bindir}/dog
%attr(755,root,root) %{_sbindir}/sheep
%attr(755,root,root) %{_sbindir}/sheepfs
%attr(755,root,root) %{_sbindir}/shepherd
%dir /var/lib/sheepdog
%attr(754,root,root) /etc/rc.d/init.d/sheepdog
%{systemdunitdir}/sheepdog.service
%{_mandir}/man8/dog.8*
%{_mandir}/man8/sheep.8*
%{_mandir}/man8/sheepfs.8*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/dog

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsheepdog.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/sheepdog

%files static
%defattr(644,root,root,755)
%{_libdir}/libsheepdog.a
