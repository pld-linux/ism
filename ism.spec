Summary:	Intel Server Management
Summary(pl):	Intel Server Management - oprogramowanie do zarz±dzania serwerem
Name:		ism
Version:	5.5.7
Release:	1
License:	restricted, non-distributable
Group:		Applications/System
Source0:	ftp://aiedownload.intel.com/df-support/6940/eng/ism%(echo %{version} | tr -d .)_build2.exe
# NoSource0-md5:	cbd5b6877fbeb0af718823c60fb155f6
Source1:	%{name}-cli.init
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

%description cli
Command Line Interface (CLI) provides the interface to the Serial Over
Lan service as an interface for platform control.

%description cli -l pl
CLI dostarcza interfejs do us³ugi Serial over LAN jako interfejs do
sterowania platform±.

%prep
%setup -q -c -T
unzip -q %{SOURCE0}

%build
rpm2cpio Software/linux/cli/8.0/*.rpm | cpio -i -d

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sbindir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dpcproxy
install usr/local/cli/* $RPM_BUILD_ROOT%{_sbindir}

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
%doc License.txt
%attr(754,root,root) /etc/rc.d/init.d/dpcproxy
%attr(755,root,root) %{_sbindir}/dpc*
