# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod

%global debug_package %{nil}

Name:       atlantic-kmod
Version:    6.15.4
Release:    1%{?dist}
Summary:    Kernel driver for Aquantia AQtion with WOL support
License:    GPL-2.0-only

Source0:    linux-%{version}-atlantic.tar.xz
Patch0:     atlantic-atl2-wol.patch

# Get the needed BuildRequires (in parts depending on what we build for):
BuildRequires:  kmodtool

# kmodtool does its magic here:
%{expand:%(kmodtool --target %{_target_cpu} --repo zeroepoch.com --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Kernel driver for the Marvell (formerly Aquantia) AQtion multi-gigabit NICs.
This build of the atlantic driver has WOL support for ATL2 devices like the AQC113(C).

%prep
# Error out if there was something wrong with kmodtool:
%{?kmodtool_check}
# Print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --repo zeroepoch.com --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -p1 -n linux-%{version}

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr drivers _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}/
        %make_build -C "${kernel_version##*___}" M=$(pwd)/drivers/net/ethernet/aquantia/atlantic modules
    popd
done

%install
for kernel_version in %{?kernel_versions}; do
    # Print out modules that are getting built:
    find _kmod_build_${kernel_version%%___*} -name "*.ko"
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 \
        _kmod_build_${kernel_version%%___*}/drivers/net/ethernet/aquantia/atlantic/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Sun Jun 29 2025 Eric Work <work.eric@gmail.com> - 6.15.4-1
- Update to 6.15.4

* Sat Jun 14 2025 Eric Work <work.eric@gmail.com> - 6.14.11-1
- First build.
