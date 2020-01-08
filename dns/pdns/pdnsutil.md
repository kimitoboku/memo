---
layout: post
title: pdnsutil
---

PowerDNSの状態やゾーンを管理するコマンド．
動作としては，PowerDNSのバックエンドのデータベースの操作を行う．
`pdns_control` はPowerDNSにコマンドを送信するための物なので用途が違う．
PowerDNSのバックエンドのデータベースの操作が可能なので，Slaveの管理や，TSIG KEYの管理などを行える．
また，元々は `pdnssec` というコマンドであり，DNSSECまわりの鍵の追加なども行える．
自分はDNSSECが好きではないので，見なかった事にする．


## Slaveの管理
PowerDNSのデータベース系のバックエンドでは `domainmetadata` というテーブルにゾーンのメタデータを格納している．
このテーブルにNofity先や転送の許可などを行うことで，PowerDNSのSlaveの管理を行える，

`pdnsutil` コマンドを用いて以下のように設定を行うことが出来る．
```console
$ pdnsutil set-meta example.com. ALLOW-AXFR-FROM 1.1.1.1
$ pdnsutil set-meta example.com. ALSO-NOTIFY 1.1.1.1
```
これらのコマンドを実行すると， `domainmetadata` には以下のようにデータが登録される．
```
MariaDB [pdns]> select id, name from domains where name='example.com';
+----|-------------+
| id | name        |
+----|-------------+
|  9 | example.com |
+----|-------------+
1 row in set (0.00 sec)

MariaDB [pdns]> select * from domainmetadata;
+----|-----------|-----------------|------------+
| id | domain_id | kind            | content    |
+----|-----------|-----------------|------------+
|  8 |         9 | ALLOW-AXFR-FROM | 1.1.1.1    |
|  9 |         9 | ALSO-NOTIFY     | 1.1.1.1    |
+----|-----------|-----------------|------------+
2 rows in set (0.00 sec)

```


`pdnsutil` は複数の値を登録する事も出来る．
```console
$ pdnsutil set-meta example.com. ALLOW-AXFR-FROM 1.1.1.1 2.2.2.2 3.3.3.3
$ pdnsutil set-meta example.com. ALSO-NOTIFY  1.1.1.1 2.2.2.2 3.3.3.3
```
これらのコマンドを実行すると，データベースは以下のようになる
```
MariaDB [pdns]> select * from domainmetadata;
+----|-----------|-----------------|------------+
| id | domain_id | kind            | content    |
+----|-----------|-----------------|------------+
| 10 |         9 | ALLOW-AXFR-FROM | 1.1.1.1    |
| 11 |         9 | ALLOW-AXFR-FROM | 2.2.2.2    |
| 12 |         9 | ALLOW-AXFR-FROM | 3.3.3.3    |
| 13 |         9 | ALSO-NOTIFY     | 1.1.1.1    |
| 14 |         9 | ALSO-NOTIFY     | 2.2.2.2    |
| 15 |         9 | ALSO-NOTIFY     | 3.3.3.3    |
+----|-----------|-----------------|------------+
6 rows in set (0.00 sec)
```


また， `pdnsutil` は，実行の羃等性が担保されているので，現状，3つのSlaveがある状態で，Slaveの個数を2つに減らすようにコマンドを実行した場合には正しくデータベースの削除も行なってくれる．
以下のコマンドを実行する
```console
$ pdnsutil set-meta example.com. ALLOW-AXFR-FROM 1.1.1.1 3.3.3.3
$ pdnsutil set-meta example.com. ALSO-NOTIFY  1.1.1.1 3.3.3.3
```
データベースは以下のようになる．
```
MariaDB [pdns]> select * from domainmetadata;
+----|-----------|-----------------|------------+
| id | domain_id | kind            | content    |
+----|-----------|-----------------|------------+
| 16 |         9 | ALLOW-AXFR-FROM | 1.1.1.1    |
| 17 |         9 | ALLOW-AXFR-FROM | 3.3.3.3    |
| 18 |         9 | ALSO-NOTIFY     | 1.1.1.1    |
| 19 |         9 | ALSO-NOTIFY     | 3.3.3.3    |
+----|-----------|-----------------|------------+
4 rows in set (0.01 sec)
```
となり，便利にSlaveを管理する事が出来る．
AnsibleなどでSlaveを管理したい場合は，MySQLを直接扱うよりも，pdnsutilコマンドを実行した方が安全．
また，存在しないゾーンに対して， `pdnsutil` コマンドを使用しても，データベースに登録されないだけなので，たいした問題はない．
