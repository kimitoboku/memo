---
layout: post
title: tcpdump
---

パケットをキャプチャするためのツール
オプションをよく忘れる．
tsharkの方が微妙に使い勝手が良いので好き．

ポートやプロトコルをそのまま表示
```
$ sudo tcpdump -i eth0 -nn port 53
```
