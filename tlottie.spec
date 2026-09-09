%undefine _debugsource_packages

# Recreate the vendor archive after a snapshot bump:
#   tar xf tlottie-0.1.0-758c7cb.tar.gz
#   cd tlottie-<commit>
#   cargo vendor --locked vendor
#   tar cJf tlottie-0.1.0-vendor.tar.xz vendor
#   abb store tlottie-0.1.0-758c7cb.tar.gz tlottie-0.1.0-vendor.tar.xz

# Commit used by Telegram Desktop 7.2.7 official Linux docker
%define gitcommit 758c7cb74444f1c3c9923065c40fdb3aad8b7d60
%define gittag 758c7cb

Name:		tlottie
Version:	0.1.0
Release:	2
Summary:	Rust Lottie renderer with a C API
License:	MIT
Group:		System/Libraries
URL:		https://github.com/dkaraush/tlottie
Source0:	https://github.com/dkaraush/tlottie/archive/%{gitcommit}.tar.gz#/%{name}-%{version}-%{gittag}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz
BuildRequires:	cargo
BuildRequires:	rust

%description
tlottie is a Rust Lottie (and Telegram TGS) renderer. Telegram Desktop
7.2.7 and later need the C API static library in place of the old
rlottie backend.

This package is the 758c7cb snapshot that upstream Telegram Desktop
pins for 7.2.7.

%prep
%autosetup -p1 -n tlottie-%{gitcommit} -a1
mkdir -p .cargo
cat > .cargo/config.toml << 'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

[net]
offline = true
EOF

%build
export CARGO_HOME="$PWD/.cargo"
export CARGO_NET_OFFLINE=true
cargo rustc --offline --locked --lib --release --features c-api --crate-type staticlib

%install
install -D -m644 target/release/libtlottie.a %{buildroot}%{_libdir}/libtlottie.a
install -D -m644 include/tlottie.h %{buildroot}%{_includedir}/tlottie/tlottie.h
cat > tlottie.pc << EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: tlottie
Description: Rust Lottie renderer with a C API
Version: %{version}
Libs: -L\${libdir} -ltlottie
Cflags: -I\${includedir}/tlottie
EOF
install -D -m644 tlottie.pc %{buildroot}%{_libdir}/pkgconfig/tlottie.pc

%files
# Upstream ships no LICENSE file; Cargo.toml declares license = "MIT".
%doc README.md
%{_libdir}/libtlottie.a
%{_includedir}/tlottie
%{_libdir}/pkgconfig/tlottie.pc
