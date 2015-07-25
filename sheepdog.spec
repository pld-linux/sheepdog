# TODO:
# - more clusters support:
#   - zookeeper (http://zookeeper.apache.org/) [-lzookeeper_mt, zookeeper.h]
#   - accord (http://www.osrg.net/accord/ - available on github, no releases yet) [libacrd.pc]
# - PLDify and register init script
Summary:	Sheepdog - distributed storage system for QEMU/KVM
Summary(pl.UTF-8):	Sheepdog - rozproszony system przechowywania danych dla QEMU/KVM
Name:		sheepdog
Version:	0.9.0
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/collie/sheepdog/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	47f2381734a2e3f9ed4b10ef38254ba9
Patch0:		ix86-cpus.patch
URL:		http://www.osrg.net/sheepdog/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	corosync-devel
BuildRequires:	groff
BuildRequires:	libfuse-devel
BuildRequires:	pkgconfig
BuildRequires:	userspace-rcu-devel >= 0.6.0
ExclusiveArch:	%{ix86} %{x8664}
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-%{name}
bash-completion for sheepdog dog command.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe dopełnianie składni dla polecenia dog z pakietu sheepdog.

%prep
%setup -q -n sheepdog-sheepdog-c648986
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
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
%doc COPYING README INSTALL
%attr(755,root,root) %{_sbindir}/dog
%attr(755,root,root) %{_sbindir}/sheep
%attr(755,root,root) %{_sbindir}/sheepfs
%attr(755,root,root) %{_sbindir}/shepherd
%dir /var/lib/sheepdog
%attr(754,root,root) /etc/rc.d/init.d/sheepdog
%{_mandir}/man8/dog.8*
%{_mandir}/man8/sheep.8*
%{_mandir}/man8/sheepfs.8*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/dog
