%define	iso_md5 25b6816378904eb61d0aee7aba2991fd
%define	_ver	%(echo %{version} | tr -d .)
Summary:	Intel Server Management
Summary(pl):	Intel Server Management - oprogramowanie do zarz±dzania serwerem
Name:		ism
Version:	8.3.0
Release:	1
License:	restricted, non-distributable
Group:		Applications/System
# downloading from http://downloadfinder.intel.com/scripts-df/Product_Filter.asp?ProductID=1071
Source0:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}aa
# NoSource0-md5:	79c19ec710a578a111b519508f7eb453
NoSource:	0
Source1:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}ab
# NoSource1-md5:	7acac599f01864d733cc15ad2a39c7ee
NoSource:	1
Source2:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}ac
# NoSource2-md5:	17189944f06516a20d95fe3ffded2043
NoSource:	2
Source3:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}ad
# NoSource3-md5:	624a30eea7e8012d4cfb45c1fd2f769a
NoSource:	3
Source4:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}ae
# NoSource4-md5:	6cea4b86dbca6aa82aaeaa57d1e93b6e
NoSource:	4
Source5:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}af
# NoSource5-md5:	dabc4acb0964415cdb586e585cadc37e
NoSource:	5
Source6:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}ag
# NoSource6-md5:	7b50ab061bc49dfdba3c3055b8ece87b
NoSource:	6
Source7:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}ah
# NoSource7-md5:	55510bc5c5b3166dc14915e91ecd5ad8
NoSource:	7
Source8:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}ai
# NoSource8-md5:	d18d195baec683b3aa565191907d6a20
NoSource:	8
Source9:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}aj
# NoSource9-md5:	4233b377ea46a37f06d3fa7222cd2188
NoSource:	9
Source10:	http://aiedownload.intel.com/df-support/8590/eng/%{name}%{_ver}ak
# NoSource10-md5:	2d426246767550ee4eeae06fac1bd9f5
NoSource:	10
Source101:	%{name}-cli.init
Source102:	dpcproxy.sysconfig
BuildRequires:	cdrtools-utils
BuildRequires:	mawk
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	rpm-utils
BuildRequires:	unzip
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
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

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
