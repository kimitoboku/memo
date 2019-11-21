---
layout: post
title: /etc/gai.conf
---

LinuxでIPアドレスの優先度を設定するやつ．
Debianだと `/etc/gai.conf` に以下のように書かれてる．
```
#precedence  ::1/128       50
#precedence  ::/0          40
#precedence  2002::/16     30
#precedence ::/96          20
#precedence ::ffff:0:0/96  10
```
コメントアウトされているが，これらがデフォルトの設定値．
`::ffff:0:0/96` というが IPv6の表記でかかれたIPv4のこと．
もしIPv4の優先度をIPv6よりも上げたい場合はいかのように書けばよい．
```
precedence ::ffff:0:0/96  60
```
これで，IPv4での通信を試みるようになる．
この設定の適用には再起動が必要．
