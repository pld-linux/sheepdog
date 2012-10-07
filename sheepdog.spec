# TODO:
# - more clusters support: zookeeper [-lzookeeper_mt, zookeeper.h], accord [libacrd.pc]
# - PLDify init script
Summary:	Sheepdog - distributed storage system for QEMU/KVM
Summary(pl.UTF-8):	Sheepdog - rozproszony system przechowywania danych dla QEMU/KVM
Name:		sheepdog
Version:	0.5.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/collie/sheepdog/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b9f78edf23916fd379b70dd5504cad50
URL:		http://www.osrg.net/sheepdog/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	corosync-devel
BuildRequires:	groff
BuildRequires:	libfuse-devel
BuildRequires:	pkgconfig
BuildRequires:	userspace-rcu-devel >= 0.6.0
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

%prep
%setup -q -n collie-sheepdog-80ceb7f

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-initddir=/etc/rc.d/init.d
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/collie
%attr(755,root,root) %{_sbindir}/sheep
%attr(755,root,root) %{_sbindir}/sheepfs
%attr(754,root,root) /etc/rc.d/init.d/sheepdog
%{_mandir}/man8/collie.8*
%{_mandir}/man8/sheep.8*
%{_mandir}/man8/sheepfs.8*
