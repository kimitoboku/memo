# sysctl

カーネルのパラメータの所得や値の変更などを行えるコマンド。
たまにつまるので覚えておく

## すべての値を所得
```console
$ sysctl -a
$ sysctl -A # 表形式
```

## 特定の値のみを表示
```
$ sysctl -n net.ipv4.tcp_syncookies
1
```

## 値を設定する
```conole
$ sysctl -w net.ipv4.tcp_syncookies=1
```

## ファイルからカーネルパラメータを設定する
```console
$ sysctl -p hoge.conf #指定しなければ /etc/sysctl.confから読み込んでくれる
```

## sysctlの永続化
`/etc/sysctl.conf` に値の組み合わせを書いておくか、 `/etc/sysctl.d/` 以下に設定を分けても記述出来る。
設定はキーとバリューで書くだけ
```
net.ipv4.tcp_syncookies = 1
```

あとは普通に追記してもよい
```console
$ sysctl -w net.ipv4.tcp_syncookies=1 >> /etc/sysctl.conf
```

## よく使うパラメータ

| パラメータ                        | 説明                                                                         |
|-----------------------------------|------------------------------------------------------------------------------|
| `fs.file-max`                     | ファイルディスクリプタの最大数                                               |
| `vm.swappiness`                   | メモリのスワップをどの程度の頻度で行うか。 値が高いほど高頻度で行うらしい    |
| `net.ipv4.tcp_fin_timeout `       | TCPのFINメッセージ受信からtimeoutまでの時間                                  |
| `net.ipv4.conf.default.rp_filter` | 入力インターフェースを出力インターフェースが異なるパケットを破棄するかどうか |
| `kernel.panic`                    | カーネルパニック後に再起動するかどうか                                       |
| `net.ipv4.ip_local_port_range`    | TCPの受信ポートのレンジ                                                      |



- [Index of /doc/Documentation/sysctl/](https://www.kernel.org/doc/Documentation/sysctl/)
