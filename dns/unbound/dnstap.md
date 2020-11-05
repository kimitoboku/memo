---
layout: post
title: unboundでdnstapを使う
---

unboundでdnstapを使おうとして，久々に使ったらちょっとつまったのでメモ

unboundをdnstap付きでビルドするには以下のようにビルドオプションを指定する必要がある．
```
% ./configure --enable-dnstap
% make
```

コンフィグには以下のように記述する．
```
dnstap:
    dnstap-enable: yes
    dnstap-socket-path: "/var/run/unbound/dnstap.sock"
    dnstap-send-identity: yes
    dnstap-send-version: yes
    dnstap-log-client-query-messages: yes
    dnstap-log-client-response-messages: yes
    dnstap-log-forwarder-query-messages: yes
    dnstap-log-forwarder-response-messages: yes
    dnstap-log-resolver-query-messages: yes
    dnstap-log-resolver-response-messages: yes
```
この `yes` となっている項目をdnstapに流してくれる．

dnstapコマンドを取得する．
```
% go get -u github.com/dnstap/golang-dnstap/dnstap
```

dnstapコマンドを実行してクエリを確認する
```
$ sudo -u unbound dnstap -u /var/run/unbound/dnstap.sock
dnstap: opened input socket /var/run/unbound/dnstap.sock
dnstap.FrameStreamSockInput: accepted a socket connection
17:37:09.180934 CQ 10.231.216.119 UDP 40b "example.com." IN A
17:37:09.180962 CR 10.231.216.119 UDP 56b "example.com." IN A
```
unboundユーザで実行するのを忘れがち

nsdの場合は `nsd` ユーザで実行しよう．
