---
layout: post
title: rpmコマンド
---

# パッケージによりインストールされるファイルの一覧
```
$ rpm -ql
/etc/logrotate.d/named
/etc/named
/etc/named.conf
/etc/named.iscdlv.key
/etc/named.rfc1912.zones
/etc/named.root.key
/etc/rndc.conf
/etc/rndc.key
/etc/rwtab.d/named
....
```



# ファイルをインストールしたパッケージを表示
```
$ rpm -qf /usr/sbin/named
bind-9.11.4-9.P2.el7.x86_64
```

# パッケージの依存関係の確認
```
$ rpm -qR bind
/bin/bash
/bin/sh
/bin/sh
/bin/sh
/bin/sh
/bin/sh
/usr/bin/python
bind-libs(x86-64) = 32:9.11.4-9.P2.el7
bind-libs-lite(x86-64) = 32:9.11.4-9.P2.el7
config(bind) = 32:9.11.4-9.P2.el7
coreutils
glibc-common
grep
libGeoIP.so.1()(64bit)
libbind9.so.160()(64bit)
libc.so.6()(64bit)
libc.so.6(GLIBC_2.14)(64bit)
libc.so.6(GLIBC_2.2.5)(64bit)
libc.so.6(GLIBC_2.3)(64bit)
libc.so.6(GLIBC_2.3.4)(64bit)
libc.so.6(GLIBC_2.4)(64bit)
libcap.so.2()(64bit)
libcom_err.so.2()(64bit)
libcrypto.so.10()(64bit)
libcrypto.so.10(OPENSSL_1.0.2)(64bit)
libcrypto.so.10(libcrypto.so.10)(64bit)
libdl.so.2()(64bit)
libdl.so.2(GLIBC_2.2.5)(64bit)
libdns.so.1102()(64bit)
libgssapi_krb5.so.2()(64bit)
libisc.so.169()(64bit)
libisccc.so.160()(64bit)
libisccfg.so.160()(64bit)
libk5crypto.so.3()(64bit)
libkrb5.so.3()(64bit)
liblwres.so.160()(64bit)
libm.so.6()(64bit)
libpthread.so.0()(64bit)
libpthread.so.0(GLIBC_2.2.5)(64bit)
libselinux-utils
libselinux-utils
libxml2.so.2()(64bit)
libxml2.so.2(LIBXML2_2.4.30)(64bit)
libxml2.so.2(LIBXML2_2.6.0)(64bit)
libxml2.so.2(LIBXML2_2.6.3)(64bit)
libz.so.1()(64bit)
policycoreutils-python
policycoreutils-python
python(abi) = 2.7
python-ply
rpmlib(CompressedFileNames) <= 3.0.4-1
rpmlib(FileDigests) <= 4.6.0-1
rpmlib(PartialHardlinkSets) <= 4.0.4-1
rpmlib(PayloadFilesHavePrefix) <= 4.0-1
rtld(GNU_HASH)
selinux-policy
selinux-policy
selinux-policy-base
selinux-policy-base
shadow-utils
shadow-utils
systemd
systemd
systemd
rpmlib(PayloadIsXz) <= 5.2-1

```


# インストールしているパッケージの一覧
```
$ rpm -qa
iputils-20160308-10.el7.x86_64
automake-1.13.4-3.el7.noarch
numactl-2.0.12-3.el7.x86_64
grub2-common-2.02-0.80.el7.centos.noarch
....
```
