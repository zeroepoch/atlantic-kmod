Name:           atlantic-kmod-common
Version:        6.15.4
Release:        1%{?dist}
Summary:        Atlantic common package
License:        GPL-2.0-only
BuildArch:      noarch

Requires:       atlantic-kmod = %{version}

%description
Common package for the Atlantic kernel module with WOL support.
Currently empty to satisfy akmod dependency.

%files

%changelog
* Sun Jun 29 2025 Eric Work <work.eric@gmail.com> - 6.15.4-1
- Update to 6.15.4

* Sat Jun 14 2025 Eric Work <work.eric@gmail.com> - 6.14.11-1
- Initial packaging.
