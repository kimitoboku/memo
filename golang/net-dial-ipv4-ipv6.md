---
layout: post
title: Go言語のnet.DialのIPv4とIPv6の選択について
---

Go言語の `net.Dial` は以下のようにしてTCPなどのコネクションを作成する．
```go
conn, err := net.Dial("tcp", "example.com:80")
if err != nil {
	// handle error
}
```

この時， `example.com` が `AAAA` レコードと `A` レコードの両方のレコードを持っていた場合に，Go言語がどちらを選択するのか調査した．

# TL;DR
IPv6が自分のマシンに割り当てらている場合はIPv6を優先して使用する．
IPv6からIPv4へのFast Fallbackはデフォルトのコネクションや `net/http` のclientでは動作しないので，少し手を入れてあげる必要がある


# 本編
## 名前解決
net.Dialの中で接続先を決定するための，名前解決は，Unixにおいては `func (r *Resolver) goLookupIPCNAMEOrder(ctx context.Context, name string, order hostLookupOrder) (addrs []IPAddr, cname dnsmessage.Name, err error)` という関数で行なわれる．
- [go/dnsclient_unix.go at b5c66de0892d0e9f3f59126eeebc31070e79143b · golang/go](https://github.com/golang/go/blob/b5c66de0892d0e9f3f59126eeebc31070e79143b/src/net/dnsclient_unix.go#L566-L728)
この関数は `A` と `AAAA` レコードの両方の問合せを行う．

qtypesに2つのタイプを指定する．
```go
qtypes := [...]dnsmessage.Type{dnsmessage.TypeA, dnsmessage.TypeAAAA}
```

そして，それぞれに問合せを行う．
```go
for _, qtype := range qtypes {
    queryFn(fqdn, qtype)
}
```

そして，応答は `addrs` という `[]IPAddr` という型の変数に格納される．
Go言語において `IPAddr` という型は IPv4，IPv6の何れの型も格納可能な型になっている．

そして最終的に， `addrs` を `sortByRFC6724` という関数を用いて， `RFC6724` にならってソートした形式でアドレスのリストを返答する．
`RFC6724` は基本的にホストにIPv6が割り当てられていた場合にはIPv6が優先される．
よって，基本的には IPv6が先頭に来たリストが返される．


## 接続先決定
`net.Dial` の実際の接続は `func (d *Dialer) DialContext(ctx context.Context, network, address string) (Conn, error)` 関数の中で行なわれる．

この関数の中の，以下の処理で接続先の優先度を決定している．
```go
var primaries, fallbacks addrList
if d.dualStack() && network == "tcp" {
    primaries, fallbacks = addrs.partition(isIPv4)
} else {
    primaries = addrs
}
```
もし，DIalがDualStackを使う設定でTCPならば， アドレスのリストを `primaries` と `fallbacks` 分割する．
そうでないならば，アドレスのリストをそのまま `primaries` とする．

DualStackでTCPの場合はアドレスを2つに分割する．
`addrs.partition` 関数は，リストをIPv6とIPv4に分割し，リストの先頭にある方を `primaries` として返す．
よって，ホストにIPv6が割り当てられている環境では，名前解決時にIPv6がリストの先頭に設定されているため， IPv6アドレスが `primaries` に設定される．
また，そうでない場合はアドレスのリストがそのまま `primaries` となるので，IPv6が先頭に設置される．

最終的に接続は以下のように行なわれる
```go
var c Conn

if len(fallbacks) > 0 {
    c, err = sd.dialParallel(ctx, primaries, fallbacks)
} else {
    c, err = sd.dialSerial(ctx, primaries)
}
if err != nil {
    return nil, err
}
```
それぞれダイアルし，コネクションが返答される．

## IPv6からIPv4へのFallBack
dualstackがOnになるかどうかの判断は，`Dialer` 構造体の `FallbackDelay` という変数に依存する．
この変数の値が `0` より大きい場合には， `d.dualStack()` がTrueになり，`Happy Eyeballs` と呼ばれる， `RFC 6555` で定義された IPv6通信とIPv4通信で早く応答が帰って来た方を通信に使用するという処理をする．
ただ，デフォルトのダイアルでは，以下のように `Dialer` 構造体を使用している．
```go
func Dial(network, address string) (Conn, error) {
    var d Dialer
    return d.Dial(network, address)
}
```
よって，構造体はゼロ初期化されるので， `FallbackDelay` の値は， `0` になるので，dualstackは動作しない．
よって，Serialにアドレスのリストを前から順に接続施行する．

もし，DualStackを使用したい場合は，以下のように構造体の初期化時に設定をするDailを自作する方が良い．
```go
func myDial(network, address string) (Conn, error) {
	d := Dialer {FallbackDelay: time.Millisecond}
	return d.Dial(network, address)
}
```

また， `net/http` などの場合は以下のように標準のclientに手を入れる事でdualstackを使用する事が出来る．
```go
var myTransport = &http.Transport{
  Dial: (&net.Dialer{
    FallbackDelay: time.Millisecond,
  }).Dial,
}
var myClient = &http.Client{
    Transport: myTransport,
}
res, _ := myClient.Get(url)
```


