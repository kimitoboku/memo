---
layout: post
title: Bindにおけるゾーン転送のtimeoutについて
---

Bindのゾーン転送のtimeoutについてひっかかったのでメモ

Bindはゾーン転送を行っている間にNotifyなどを受信してもゾーン転送が終了するまではNotifyなどを無視する．
例えば，ゾーン転送中に問題が発生し，正常に行えない状態である場合にはtimeoutになるまでは，新規のゾーン転送が一切行われない状態になるという事である．
これらの設定が初期状態の場合だと，1時間，ゾーン情報の更新などが出来ない可能性があります．
幾つかSlaveのマシンがあって，そのうちの1台だけ新規のゾーン転送が行われない場合などは，この設定を確認してください．

という，ことで，ゾーン転送のtimeoutを指定する設定を確認した．

# masterサーバでの設定
masterサーバでのゾーン転送のtimeoutでは以下の設定が行える．
以下の設定はoptions節にも，zone節にも記述出来る．
```
max-transfer-time-out 120;
max-transfer-idle-out 60;
```
`max-transfer-time-out`  は一回のゾーン転送にかかる最大の時間で，デフォルトでは120分に設定されています．
`max-transfer-idle-out` はゾーン転送を開始するまでの待ち時間です．デフォルトでは60分に設定されています．

# slaveサーバでの設定
slaveサーバでのゾーン転送のtimeoutでは以下の設定が行える．
以下の設定はoptions節にも，zone節にも記述出来る．
```
max-transfer-time-in 120;
max-transfer-idle-in 60;
```
`max-transfer-time-in`  は一回のゾーン転送にかかる最大の時間で，デフォルトでは120分に設定されています．
`max-transfer-idle-in` はゾーン転送を開始するまでの待ち時間です．デフォルトでは60分に設定されています．