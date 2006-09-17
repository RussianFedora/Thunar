Summary: Thunar File Manager
Name: Thunar
Version: 0.4.0
Release: 0.5.rc1%{?dist}
License: GPL
URL: http://thunar.xfce.org/
Source0: http://www.xfce.org/archive/xfce-4.3.99.1/src/Thunar-0.4.0rc1.tar.bz2
Group: User Interface/Desktops
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: fam-devel
BuildRequires: libjpeg-devel
BuildRequires: libexif-devel
BuildRequires: libpng-devel >= 2:1.2.2-16
BuildRequires: desktop-file-utils >= 0.7
BuildRequires: exo-devel >= 0.3.1.10
BuildRequires: startup-notification-devel >= 0.4
BuildRequires: intltool gettext
BuildRequires: dbus-glib-devel 
BuildRequires: hal-devel
BuildRequires: pcre-devel
BuildRequires: xfce4-panel-devel
BuildRequires: freetype-devel
BuildRequires: pkgconfig
BuildRequires: libxslt
BuildRequires: GConf2-devel
BuildRequires: gtk-doc

%description
Thunar is a new modern file manager for the Xfce Desktop Environment. 
It has been designed from the ground up to be fast and easy-to-use. 
Its user interface is clean and intuitive, and does not include any
confusing or useless options. Thunar is fast and responsive with a 
good start up time and directory load time.

%package devel
Summary: Development tools for Thunar file manager
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: exo-devel >= 0.3.1.10

%description devel
libraries and header files for the Thunar file manager.

%prep
%setup -q -n %{name}-%{version}rc1

%build
%configure --enable-dbus --enable-final --enable-xsltproc --enable-gtk-doc
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}

make -C examples distclean

# 2 of the example files need to not be executable 
# so they don't pull in dependencies. 
chmod 644 examples/thunar-file-manager.py
chmod 644 examples/xfce-file-manager.py

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/thunarx-1/*.la

# remove the tpa plugin and desktop if it's present. 
rm -f $RPM_BUILD_ROOT/%{_libexecdir}/xfce4/panel-plugins/thunar-tpa
rm -f $RPM_BUILD_ROOT/%{_datadir}/xfce4/panel-plugins/thunar-tpa.desktop

%find_lang Thunar

rm -f ${RPM_BUILD_ROOT}%{_datadir}/applications/Thunar-bulk-rename.desktop
desktop-file-install --vendor fedora                            \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --add-category X-Fedora                                 \
        Thunar-bulk-rename.desktop

rm -f ${RPM_BUILD_ROOT}%{_datadir}/applications/Thunar-folder-handler.desktop
desktop-file-install --vendor fedora                            \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --add-category X-Fedora                                 \
        Thunar-folder-handler.desktop

rm -f ${RPM_BUILD_ROOT}%{_datadir}/applications/Thunar.desktop
desktop-file-install --vendor fedora                            \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --add-category X-Fedora                                 \
        Thunar.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
/sbin/ldconfig
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f Thunar.lang
%defattr(-,root,root,-)
%doc README TODO ChangeLog NEWS INSTALL COPYING AUTHORS HACKING THANKS
%doc docs/README.gtkrc 
%doc docs/README.thunarrc 
%doc docs/README.volumes 
%doc docs/ThumbnailersCacheFormat.txt
# exclude docs that we have moved to the above
%exclude %{_datadir}/doc/Thunar/README.gtkrc
%exclude %{_datadir}/doc/Thunar/README.thunarrc
%exclude %{_datadir}/doc/Thunar/README.volumes
%exclude %{_datadir}/doc/Thunar/ThumbnailersCacheFormat.txt
%{_bindir}/Thunar
%{_bindir}/thunar
%{_libdir}/libthunar*.so.*
%{_libdir}/thunarx-1/thunar*.so
%{_libexecdir}/ThunarBulkRename
%{_libexecdir}/ThunarHelp
%{_libexecdir}/thunar-sendto-email
%{_libexecdir}/thunar-vfs-font-thumbnailer-1
%{_libexecdir}/thunar-vfs-mime-cleaner-1
%{_libexecdir}/thunar-vfs-pixbuf-thumbnailer-1
%{_libexecdir}/thunar-vfs-update-thumbnailers-cache-1
%dir %{_datadir}/Thunar/
%dir %{_datadir}/Thunar/sendto/
%{_datadir}/Thunar/sendto/thunar-sendto-email.desktop
%{_datadir}/applications/fedora-Thunar-bulk-rename.desktop
%{_datadir}/applications/fedora-Thunar-folder-handler.desktop
%{_datadir}/applications/fedora-Thunar.desktop
%{_datadir}/dbus-1/services/org.xfce.FileManager.service
%{_datadir}/dbus-1/services/org.xfce.Thunar.service
%{_datadir}/doc/Thunar/
%{_datadir}/icons/hicolor/16x16/apps/Thunar.png
%{_datadir}/icons/hicolor/16x16/stock/navigation/stock_thunar-shortcuts.png
%{_datadir}/icons/hicolor/16x16/stock/navigation/stock_thunar-templates.png
%{_datadir}/icons/hicolor/24x24/apps/Thunar.png
%{_datadir}/icons/hicolor/48x48/apps/Thunar.png
%{_datadir}/icons/hicolor/scalable/apps/Thunar.svg
%{_datadir}/pixmaps/Thunar
# disable trash plugin for now because it doesn't build with 4.3.2
#%{_datadir}/xfce4/panel-plugins/thunar-tpa.desktop
#%{_libexecdir}/xfce4/panel-plugins/thunar-tpa
%{_mandir}/man1/Thunar.1*
%dir %{_sysconfdir}/xdg/Thunar
%config(noreplace) %{_sysconfdir}/xdg/Thunar/uca.xml

%files devel
%defattr(-,root,root,-)
%doc examples
%{_includedir}/thunar-vfs-1
%{_includedir}/thunarx-1
%{_libdir}/libthunar*.so
%{_libdir}/pkgconfig/thunar-vfs-1.pc
%{_libdir}/pkgconfig/thunarx-1.pc
%{_datadir}/gtk-doc/html/*

%changelog
* Sat Sep 16 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.5.rc1
- Remove duplicate thunar-sendto-email.desktop entry from files. 

* Fri Sep 15 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.4.rc1
- Added Requires: exo-devel >= 0.3.1.10 to devel. 
- exclude docs moved from datadir to docs
- Fixed datdir including files twice

* Thu Sep 14 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.3.rc1
- Cleaned up BuildRequires some more
- Disabled tpa plugin and desktop for now
- Moved some files from doc/Thunar to be %%doc
- Changed man to use wildcard in files
- Added examples to devel subpackage
- Made sure some examples are not executable. 

* Tue Sep 12 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.2.rc1
- Added some BuildRequires
- Added --with-gtkdoc and gtkdoc files to devel

* Wed Sep  6 2006 Kevin Fenzi <kevin@tummy.com> - 0.4.0-0.1.rc1
- Inital package for fedora extras

