%define debug_package %{nil}
Name:		zeromq-ada
Version:	3.2.0
Release:	1%{?dist}
Summary:	Ada binding for zeromq
Group:      System Environment/Libraries
License:    GPLv2+
URL:        http://zeromq.org
## Source from github. for get source use 
## git clone https://landgraf@github.com/landgraf/zeromq-Ada.git
## tar -czvf zeromq-ada-2.24032011.tar.gz zeromq-Ada
Source0:    %{name}-24032011git.tar.gz
## Use shared libs instead static
Patch0:     %{name}-libdir.patch
## Use directories.gpr
Patch1:     %{name}-fedora.patch
BuildRequires: fedora-gnat-project-common >= 2 zeromq-devel >= 2.1
BuildRequires:  chrpath
Requires:    zeromq >= 2.1
# gcc-gnat only available on these:
ExclusiveArch: %{ix86} x86_64 ia64 ppc ppc64 alpha

%description
Ada bindings for zeromq

%package devel
Summary:        Devel package for Ada binding for zeromq
Group:          System Environment/Libraries
License:        GPLv2+
Requires:       fedora-gnat-project-common  >= 2
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zeromq >= 2.1

%description devel
%{summary}
%prep
%setup -q -n zeromq-Ada
%patch0 -p1
%patch1 -p1

%build
make %{?_smp_mflags}  GNATFLAGS="%{GNAT_optflags}" 
## for tests aunit needed


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} ADA_PROJECT_DIR=%{_GNAT_project_dir}  GNATFLAGS="%{GNAT_optflags}"
rm -f %{buildroot}/%{_libdir}/zmq/static/libzmqAda.a
rm -rf %{buildroot}/%{_libdir}/zmq/static
chrpath --delete %{buildroot}%{_libdir}/zmq/relocatable/libzmqAda.so.%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README COPYING
%dir %{_libdir}/zmq
%dir %{_libdir}/zmq/relocatable
%{_libdir}/zmq/relocatable/libzmqAda.so.%{version}
%{_libdir}/libzmqAda.so.*


%files devel
%defattr(-,root,root,-)
%{_libdir}/zmq/relocatable/libzmqAda.so
%{_libdir}/libzmqAda.so
%dir %{_includedir}/zmq/
%{_includedir}/zmq/*.adb
%{_includedir}/zmq/*.ads
%{_GNAT_project_dir}/zmq.gpr
%{_libdir}/zmq/relocatable/*.ali
%{_datadir}/zmq/*

%changelog
* Sun Sep 23 2012 Pavel Zhukov <landgraf@fedoraproject.org> - 2.1.0-9.24032011git
- Fix gpr path

* Sun Sep 23 2012 Pavel Zhukov <landgraf@fedoraproject.org> - 2.1.0-8.24032011git
- Fix libraries symlinks
- Add usrmove patch

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-7.24032011git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May 05 2011 Dan Horák <dan[at]danny.cz> - 2.1.0-6.24032011git
- updated the supported arch list

* Fri Apr 29 2011 Pavel Zhukov <landgraf@fedoraproject.org> - 2.1.0-4.24032011git
- Create shared libraries path
- Fix license tag
- Fix spec errors

* Thu Mar 24 2011 Pavel Zhukov <landgraf@fedoraproject.org> - 2.1.0-1.24032011git
- update to new commit

* Wed Feb 2 2011 Pavel Zhukov <pavel@zhukoff.net> - 2.0.10-02022011git
- Initial package
