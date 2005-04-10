%define	iso_md5 25b6816378904eb61d0aee7aba2991fd
Summary:	Intel Server Management
Summary(pl):	Intel Server Management - oprogramowanie do zarz±dzania serwerem
Name:		ism
Version:	8.3.0
Release:	0.1
License:	restricted, non-distributable
Group:		Applications/System
# downloading from http://downloadfinder.intel.com/scripts-df/Product_Filter.asp?ProductID=1071
Source0:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)aa
# NoSource0-md5:	52ea53ae2cf93247ca07c0cf257367b6
NoSource:	0
Source1:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)ab
# NoSource1-md5:	9bca501dba89dd7720913124c3ade71a
NoSource:	1
Source2:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)ac
# NoSource2-md5:	f1e8e2b09568f87e65d2371a5899c688
NoSource:	2
Source3:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)ad
# NoSource3-md5:	76950c98eb18b0c1aaf00335088eaa12
NoSource:	3
Source4:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)ae
# NoSource4-md5:	26e3e232228b19c0c73ad62ba76bcd9b
NoSource:	4
Source5:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)af
# NoSource5-md5:	654e183a32c59a4a47f9c457cfc5643d
NoSource:	5
Source6:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)ag
# NoSource6-md5:	783e1dd01f73b23109e87e9970434b58
NoSource:	6
Source7:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)ah
# NoSource7-md5:	55510bc5c5b3166dc14915e91ecd5ad8
NoSource:	7
Source8:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)ai
# NoSource8-md5:	d18d195baec683b3aa565191907d6a20
NoSource:	8
Source9:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)aj
# NoSource9-md5:	4233b377ea46a37f06d3fa7222cd2188
NoSource:	9
Source10:	http://aiedownload.intel.com/df-support/8590/eng/ism%(echo %{version} | tr -d .)ak
# NoSource10-md5:	2d426246767550ee4eeae06fac1bd9f5
NoSource:	10
Source101:	%{name}-cli.init
Source102:	dpcproxy.sysconfig
BuildRequires:	rpm-utils
BuildRequires:	unzip
BuildRequires:	mawk
BuildRequires:	cdrtools-utils
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Intel Server Management Software.

%description -l pl
Intel Server Management - oprogramowanie do zarz±dzania serwerem.

%package cli
Summary:	Serial Over Lan service
Summary(pl):	Us³uga Serial over LAN
Group:		Applications/System

%description cli
Command Line Interface (CLI) provides the interface to the Serial Over
Lan service as an interface for platform control.

%description cli -l pl
CLI dostarcza interfejs do us³ugi Serial over LAN jako interfejs do
sterowania platform±.

%prep
%setup -q -c -T

(
cat %{SOURCE0} &&
cat %{SOURCE1} &&
cat %{SOURCE2} &&
cat %{SOURCE3} &&
cat %{SOURCE4} &&
cat %{SOURCE5} &&
cat %{SOURCE6} &&
cat %{SOURCE7} &&
cat %{SOURCE8} &&
cat %{SOURCE9} &&
cat %{SOURCE10} ) > iso.tmp

md5=$(md5sum -b < iso.tmp | awk '{print $1}')
if [ "$md5" != "%{iso_md5}" ]; then
	echo >&2 "iso md5 mismatch: got $md5, need %{iso_md5}"
	exit 1
fi
mv -f iso.tmp %{name}-%{version}.iso

%build
isoinfo -i %{name}-%{version}.iso -x /ISM/SOFTWARE/LINUX/32BIT/CLI/EL3.0/CLI-2~1.RPM > cli.rpm
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
if [ -f /var/lock/subsys/dpcproxy ]; then
	/etc/rc.d/init.d/dpcproxy restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/dpcproxy start\" to start dpcproxy server" 1>&2
fi

%preun cli
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/dpcproxy ]; then
		/etc/rc.d/init.d/dpcproxy stop >&2
	fi
	/sbin/chkconfig --del dpcproxy
fi

%clean
rm -rf $RPM_BUILD_ROOT

#%files
#%defattr(644,root,root,755)

%files cli
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dpcproxy
%attr(754,root,root) /etc/rc.d/init.d/dpcproxy
%attr(755,root,root) %{_sbindir}/dpc*
