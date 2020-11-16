---
layout: post
title: unboundの権威サーバ機能の使い方
---

近年のUnboundは権威サーバ機能が追加さ、DNS Authとしてゾーンをホスト出来るようになった。
例えば、ホスト名の管理用のシステムからゾーン転送を受信してUnboundでstub-zoneを使用しバックエンドに問い合わせることなく、Unboundが応答を返せるようになった。
これにより、例えば、ホスト名が追加された場合に誤った問い合わせでNXDOMAINが帰りネガティブキャッシュで数分間ホスト名の解決が出来ないといった状態になる事を防ぐ事が出来る。

設定方法は以下の通りである。
```
auth-zone:
    name: "test.corp"
    primary: 192.0.2.1
    allow-notify: 192.0.2.1
    fallback-enabled: yes
    zonefile: /etc/unbound/zones/test.corp.zone
```
`fallback-enabled: yes` を使用するとレコードが存在しない場合にUnboundがresolverとして動作しインターネットに問い合わせるようになる。


この設定を行い、unboundに `test.corp` を問い合わせるとゾーンの内容により以下のように応答が返る。
```console
$ dig @192.0.2.2 test.corp

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-16.P2.el7_8.6 <<>> @10.127.85.31 test.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7247
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;test.corp.                      IN      A

;; ANSWER SECTION:
test.corp.               600     IN      A       192.0.2.1

;; Query time: 0 msec
;; SERVER: 10.127.85.31#53(10.127.85.31)
;; WHEN: Mon Nov 16 18:45:45 JST 2020
;; MSG SIZE  rcvd: 53

```
フラグとしては `AA` グラフが追加応答を返す。

また、`CNAME` ではBindでCacheとAuthを共存させた場合と異なる動作を行う。
UnboundにCNAMEのあるレコードの問い合わせを行うと以下のような応答が帰って来る。
```
$ dig @192.0.2.2 www.test.corp

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-16.P2.el7_8.6 <<>> @10.127.85.31 www.test.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 612
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;www.test.corp.                  IN      A

;; ANSWER SECTION:
www.test.corp.           600     IN      CNAME   example.com.

;; Query time: 0 msec
;; SERVER: 10.127.85.31#53(10.127.85.31)
;; WHEN: Mon Nov 16 19:03:57 JST 2020
;; MSG SIZE  rcvd: 63

```
となり、CNAMEの解決は行わずに権威サーバとしての応答を返す。


Bindの場合は以下のようにexample.comの解決まで行い、応答を返す。
```
$ dig @192.0.2.2 www.test.corp

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-16.P2.el7_8.6 <<>> @10.127.85.31 www.test.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 49154
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 2, ADDITIONAL: 5

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;www.test.corp.                  IN      A

;; ANSWER SECTION:
www.test.corp.           600     IN      CNAME   example.com.
example.com.            86391   IN      A       93.184.216.34

;; AUTHORITY SECTION:
example.com.            172789  IN      NS      a.iana-servers.net.
example.com.            172789  IN      NS      b.iana-servers.net.

;; ADDITIONAL SECTION:
a.iana-servers.net.     1789    IN      A       199.43.135.53
b.iana-servers.net.     172789  IN      A       199.43.133.53
a.iana-servers.net.     172789  IN      AAAA    2001:500:8f::53
b.iana-servers.net.     1789    IN      AAAA    2001:500:8d::53

;; Query time: 0 msec
;; SERVER: 10.127.85.31#53(10.127.85.31)
;; WHEN: Mon Nov 16 19:04:32 JST 2020
;; MSG SIZE  rcvd: 215

```

ホスト名用のゾーンの応答を返したいといった処理には問題はないが、例えば、DNS Authが落ちた場合でも内部で一部のレコードを使用したいといった処理を考えた場合には、UnboundではなくBindを選択した方が良いのではないかと思う。
