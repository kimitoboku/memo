---
layout: post
title: NetworkManagerを用いてCLIでWifiに接続
---

SSIDの一覧を表示．
```
$  nmcli device wifi list
```
SSIDや電波強度，接続する場合のセキュリティなどを表示出来る．
出力結果は，見られると困るので，割愛．

Wifiに接続
```
$ nmcli device wifi connect SSID password 'PASSWORD' ifname wlan0
デバイス 'wlan0' が '387ab442-2b5e-44c9-8c2d-3080426a0ed3' で正常にアクティベートされました。
```
これで，CLIからWiFiに接続が完了する．

Wifiからの接続を解除．
```
$ nmcli device disconnect wlan0
```

SSIDの設定を削除(次回から自動で接続されてしまうのを防ぐため)
```
$ nmcli connection delete SSID
```

たまに，外で使おうとすると忘れるのでメモ．