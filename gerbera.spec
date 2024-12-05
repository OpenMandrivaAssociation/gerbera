# set to nil when packaging a release, 
# or the long commit tag for the specific git branch
%global commit_tag %{nil}

# set with the commit date only if commit_tag not nil 
# git version (i.e. master) in format date +Ymd
%if "%{commit_tag}" != "%{nil}"
%global commit_date %(git show -s --date=format:'%Y%m%d' %{commit_tag})
%endif

# repack non-release git branches as .7z with the commit date
# in the following format <name>-<version>-<commit_date>.7z
# the short commit tag should be 7 characters long

Name:		   gerbera
Version:        2.3.0%{?commit_date:~%{commit_date}}
Release:        1
Summary:	    UPnP Media Server
Group:		  Multimedia
License:	    GPLv2
URL:		    https://github.com/gerbera/gerbera

# change the source URL depending on if the package is a release version or a git version
%if "%{commit_tag}" != "%{nil}"
Source0:        %{url}/archive/%{commit_tag}.tar.gz#/%{name}-%{version}.7z
%else
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

Source1:        config.xml
Source2:        gerbera.conf

BuildRequires:  pkgconfig(duktape)
BuildRequires:  pkgconfig(exiv2)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libebml)
BuildRequires:  pkgconfig(libffmpegthumbnailer)
BuildRequires:  pkgconfig(libmatroska)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(fmt)
BuildRequires:  pkgconfig(libupnp) >= 1.14.6
BuildRequires:  pkgconfig(pugixml)
BuildRequires:  pkgconfig(sqlite3) >= 3.7.11
BuildRequires:  pkgconfig(spdlog) >= 1.8.1
BuildRequires:  pkgconfig(taglib) >= 1.12
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  inotify-tools-devel
BuildRequires:  cmake
BuildRequires:  ninja

%description
Gerbera is a UPnP media server which allows you to stream your digital media 
through your home network and consume it on a variety of UPnP compatible 
devices.

%prep
%autosetup -p1
%cmake -G "Ninja" \
    -DWITH_JS=ON \
    -DWITH_TAGLIB=ON \
    -DWITH_MAGIC=ON \
    -DWITH_AVCODEC=ON \
    -DWITH_EXIF=OFF \
    -DWITH_EXIV2=ON \
    -DWITH_FFMPEGTHUMBNAILER=ON \
    -DWITH_INOTIFY=ON \
    -DWITH_SYSTEMD=ON \
    -DWITH_TESTS=OFF    

%build
%ninja_build -C ${CMAKE_BUILD_DIR:-build}


%install
%ninja_install -C ${CMAKE_BUILD_DIR:-build}
install -p -D -m0644 %{S:1} %{buildroot}%{_sysconfdir}/%{name}/config.xml
install -p -D -m0644 %{S:2} %{buildroot}%{_sysusersdir}/%{name}.conf
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

%check


%files
%license LICENSE.md
%doc AUTHORS CONTRIBUTING.md ChangeLog.md

%attr(-,%{name},%{name})%dir %{_sysconfdir}/%{name}/
%attr(-,%{name},%{name})%config(noreplace) %{_sysconfdir}/%{name}/*
%attr(-,%{name},%{name}) %{_localstatedir}/log/%{name}
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
%{_mandir}/man1/%{name}.1.zst
%{_datadir}/%{name}/mysql-upgrade.xml
%{_datadir}/%{name}/mysql.sql
%{_datadir}/%{name}/sqlite3-upgrade.xml
%{_datadir}/%{name}/sqlite3.sql
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/js
%dir %{_datadir}/%{name}/web
%{_datadir}/%{name}/js/*
%{_datadir}/%{name}/web/*

