---
layout: post
title: /sys/kernel/debug
---

Linuxカーネル内部のデバッグに関わる情報を参照するための物．
以下のようにマウントする．

```console
$ sudo mount -t debugfs none /sys/kernel/debug
```

以下のようにスタティックなトレースポイントのフォーマットが見れたりする．
```console
$ sudo cat /sys/kernel/debug/tracing/events/net/napi_gro_frags_entry/format
```

kprobesの一覧も見れたりする．(kprbesは仕組み的にフォーマットとかが作れたりするわけではない)
```console
$ sudo cat /sys/kernel/debug/kprobes/list
```


作り方などは以下のページが詳しい
- [カーネルモジュール作成によるlinuxカーネル開発入門 - 第三回 デバッグ用インターフェース - Qiita](https://qiita.com/satoru_takeuchi/items/d2760c32a88376e1bc4a)
