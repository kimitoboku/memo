---
layout: post
title: only-notify
---

PowerDNSはゾーンのタイプがMASTERであった場合に，NSレコードに登録されているホストに対して自動でNOTIFYを送信する．
only-nofityは自動的に送信するIPアドレスのレンジを設定する．

デフォルトでは以下の設定が入っている
```
only-notify=0.0.0.0/0, ::/0
```
つまり，NSレコードに登録されているホストが何であろうともNOTIFYを送信する．
NSレコードのホストへのNOTIFYをオフにしたい場合は，以下のように `pdns.conf` に設定を記述する．
```
only-notify=
```
only-notifyにnofityを送信しないという設定を入れても， `pdns.conf` の `also-nofity` やDBベースの `domainmetadata` において `ALSO-NOTIFY` を設定した場合は正しくNOTFYが送信される．
NOTIFYを送信する宛先を正しく管理したい場合には確実にこの設定を `pdns.conf` に記述するべき．
デフォルトの設定で動作するようになっているので，気付くのに時間がかかる．


# 参考文献
- [Authoritative Server Settings — PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/settings.html#only-notify)
