%define real_name tyton

Summary: Linux kernel module for Tyton
Name: dkms-tyton
Version: master
Release: 1%{?dist}
License: GPL
Group: System Environment/Kernel
URL: https://github.com/nbulischeck/tyton

Source: tyton-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
Requires: gcc, make, libnotify-devel, gtk3-devel, systemd-devel, libnotify, gtk3, kernel-devel
Requires(post): dkms
Requires(preun): dkms

%description
Tyton is a Linux Kernel-Mode Rootkit Hunter for kernel 4.4.0-31+

%prep
%setup -n %{real_name}-%{version}

%build

%install
%{__rm} -rf %{buildroot}

%define dkms_name tyton
%define dkms_vers %{version}-%{release}
%define quiet -v

# Kernel module sources install for dkms
%{__mkdir_p} %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_vers}/
%{__cp} -a ./* %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_vers}/

# Configuration for dkms
%{__cat} > %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_vers}/dkms.conf << 'EOF'
PACKAGE_NAME=%{dkms_name}
PACKAGE_VERSION=%{dkms_vers}
BUILT_MODULE_NAME[0]=tyton
DEST_MODULE_LOCATION[0]=/kernel/drivers/tyton
AUTOINSTALL="YES"
EOF

%clean
%{__rm} -rf %{buildroot}

%post
# Add to DKMS registry
dkms add -m %{dkms_name} -v %{dkms_vers} || :
# Rebuild and make available for the currenty running kernel
dkms build -m %{dkms_name} -v %{dkms_vers} || :
dkms install -m %{dkms_name} -v %{dkms_vers} --force || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{dkms_vers} --all || :

%files
%defattr(-, root, root, 0755)
%{_usrsrc}/%{dkms_name}-%{dkms_vers}/

%changelog
