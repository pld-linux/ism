Summary:	Intel Server Management
Summary(pl.UTF-8):	Intel Server Management - oprogramowanie do zarządzania serwerem
Name:		ism
Version:	8.40.20.141
Release:	1
License:	restricted, non-distributable
Group:		Applications/System
URL:		http://downloadfinder.intel.com/scripts-df-external/Product_Filter.aspx?ProductID=1071
Source0:	http://downloadmirror.intel.com/df-support/9546/eng/%{name}840.zip
# NoSource0-md5:	88674ce9932169580d1150dda7b458e8
NoSource:	0
Source101:	dpcproxy.init
Source102:	dpcproxy.sysconfig
BuildRequires:	cdrtools-utils
BuildRequires:	mawk
BuildRequires:	rpm-utils
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Intel Server Management Software.

%description -l pl.UTF-8
Intel Server Management - oprogramowanie do zarządzania serwerem.

%package cli
Summary:	Serial Over Lan service
Summary(pl.UTF-8):	Usługa Serial over LAN
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description cli
Command Line Interface (CLI) provides the interface to the Serial Over
Lan service as an interface for platform control.

%description cli -l pl.UTF-8
CLI dostarcza interfejs do usługi Serial over LAN jako interfejs do
sterowania platformą.

%prep
%setup -qc

%build
isoinfo -i *.iso -x /ISM/SOFTWARE/LINUX/32BIT/CLI/EL3.0/CLI-2~1.RPM > cli.rpm
rpm2cpio cli.rpm | cpio -i -d

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
install -d $RPM_BUILD_ROOT%{_sbindir}

install %{SOURCE101} $RPM_BUILD_ROOT/etc/rc.d/init.d/dpcproxy
install usr/local/cli/* $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE102} $RPM_BUILD_ROOT/etc/sysconfig/dpcproxy

%post cli
/sbin/chkconfig --add dpcproxy
%service dpcproxy restart

%preun cli
if [ "$1" = "0" ]; then
	%service dpcproxy stop
	/sbin/chkconfig --del dpcproxy
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files cli
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dpcproxy
%attr(754,root,root) /etc/rc.d/init.d/dpcproxy
%attr(755,root,root) %{_sbindir}/dpc*
