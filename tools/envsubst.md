---
layout: post
title: envsubst
---

GNU環境で環境変数を用いたテンプレートファイルなどを展開出来るコマンド。

envsubstは標準入力から環境変数として指定されている変数 `$HOGE` もしくは `${HOGE}` を置換する事が出来る。
```
$ cat nsd.conf.tmp
server:
        use-systemd: yes
        username: nsd
        zonesdir: "/etc/nsd/zones"
        logfile: "/var/log/nsd/nsd.log"
        pidfile: "/var/run/nsd/nsd.pid"
        hide-version: yes
        tcp-count: ${NSD_TCP_COUNT}
        round-robin: yes
        verbosity: ${NSD_VERBOSITY}
        zonefiles-write: ${NSD_ZONE_FILE_WRITE}
$ export NSD_TCP_COUNT=1000
$ export NSD_VERBOSITY=2
$ export NSD_ZONE_FILE_WRITE=1
$ envsubst < nsd.conf.tmp
server:
        use-systemd: yes
        username: nsd
        zonesdir: "/etc/nsd/zones"
        logfile: "/var/log/nsd/nsd.log"
        pidfile: "/var/run/nsd/nsd.pid"
        hide-version: yes
        tcp-count: 1000
        round-robin: yes
        verbosity: 2
        zonefiles-write: 1
$
```

また、ファイルの中で環境変数のようなパラメータを利用している場合(Apacheの設定ファイルなど)は引数に置換する環境変数を指定する事でその変数のみ置換を行う事が出来る。
```
$ envsubst '$$NSD_TCP_COUNT' < nsd.conf.tmp
server:
        use-systemd: yes
        username: nsd
        zonesdir: "/etc/nsd/zones"
        logfile: "/var/log/nsd/nsd.log"
        pidfile: "/var/run/nsd/nsd.pid"
        hide-version: yes
        tcp-count: 1000
        round-robin: yes
        verbosity: ${NSD_VERBOSITY}
        zonefiles-write: ${NSD_ZONE_FILE_WRITE}
$
```